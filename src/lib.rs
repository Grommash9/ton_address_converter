use pyo3::prelude::*;
use base64::{Engine, engine::{self, general_purpose}};
use rayon::prelude::*;

const BOUNCEABLE_TAG: u8 = 0x11;
const NON_BOUNCEABLE_TAG: u8 = 0x51;
const TEST_FLAG: u8 = 0x80;

#[pyfunction]
fn batch_convert_to_raw(
    py: Python<'_>,
    addresses: Vec<String>,
    chunk_size: Option<usize>
) -> PyResult<Vec<String>> {
    py.allow_threads(|| {
        let chunk_size = chunk_size.unwrap_or(1000);
        let chunks: Vec<_> = addresses.chunks(chunk_size).collect();
        
        let results: Vec<Vec<String>> = chunks.par_iter()
            .map(|chunk| {
                chunk.iter()
                    .map(|addr| friendly_to_raw(addr))
                    .collect()
            })
            .collect();
            
        Ok(results.into_iter().flatten().collect())
    })
}

#[pyfunction]
fn batch_convert_to_friendly(
    py: Python<'_>,
    addresses: Vec<String>,
    chunk_size: Option<usize>,
    bounceable: Option<bool>,
    test_only: Option<bool>,
    url_safe: Option<bool>
) -> PyResult<Vec<String>> {
    py.allow_threads(|| {
        let chunk_size = chunk_size.unwrap_or(1000);
        let chunks: Vec<_> = addresses.chunks(chunk_size).collect();
        let is_bounceable = bounceable.unwrap_or(false);
        let is_test = test_only.unwrap_or(false);
        let is_url_safe = url_safe.unwrap_or(true);
        
        let results: Vec<Vec<String>> = chunks.par_iter()
            .map(|chunk| {
                chunk.iter()
                    .map(|addr| raw_to_friendly(addr, is_bounceable, is_test, is_url_safe))
                    .collect()
            })
            .collect();
            
        Ok(results.into_iter().flatten().collect())
    })
}

fn friendly_to_raw(address: &str) -> String {
    if address.contains(':') {
        return address.to_string(); // Already in raw format
    }

    // Replace URL-safe characters back to standard base64
    let std_base64 = address.replace('-', "+").replace('_', "/");
    // Add padding if necessary
    let padded = match std_base64.len() % 4 {
        2 => format!("{}==", std_base64),
        3 => format!("{}=", std_base64),
        _ => std_base64,
    };

    let data = match general_purpose::STANDARD.decode(padded) {
        Ok(d) if d.len() == 36 => d,
        _ => return address.to_string(), // Return original if invalid
    };

    let wc = if data[1] == 0xFF { -1 } else { data[1] as i8 };
    let hash_part = &data[2..34];
    
    format!("{}:{}", wc, hex::encode(hash_part).to_lowercase())
}

fn raw_to_friendly(address: &str, is_bounceable: bool, is_test: bool, is_url_safe: bool) -> String {
    if !address.contains(':') {
        return address.to_string(); // Return if already in friendly format
    }

    let parts: Vec<&str> = address.split(':').collect();
    if parts.len() != 2 {
        return address.to_string();
    }

    let wc: i8 = parts[0].parse().unwrap_or(0);
    let hash = match hex::decode(parts[1].to_lowercase()) {
        Ok(h) if h.len() == 32 => h,
        _ => return address.to_string(),
    };

    let mut addr = Vec::with_capacity(36);
    let mut tag = if is_bounceable { BOUNCEABLE_TAG } else { NON_BOUNCEABLE_TAG };
    if is_test {
        tag |= TEST_FLAG;
    }

    addr.push(tag);
    addr.push(if wc == -1 { 0xFF } else { wc as u8 });
    addr.extend_from_slice(&hash);

    // Add CRC16
    let crc = crc16(&addr);
    addr.extend_from_slice(&crc);

    // Encode as base64
    let b64 = general_purpose::STANDARD.encode(&addr);
    
    if is_url_safe {
        b64.replace('+', "-")
            .replace('/', "_")
            .trim_end_matches('=')
            .to_string()
    } else {
        b64.trim_end_matches('=').to_string()
    }
}

fn crc16(data: &[u8]) -> [u8; 2] {
    let mut crc: u16 = 0;
    for &byte in data {
        // XOR byte into least sig. byte of crc
        crc ^= (byte as u16) << 8;
        // Loop over each bit
        for _ in 0..8 {
            if (crc & 0x8000) != 0 {
                crc = (crc << 1) ^ 0x1021;
            } else {
                crc <<= 1;
            }
        }
    }
    [(crc >> 8) as u8, crc as u8]
}

#[pymodule]
fn ton_address_converter(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(batch_convert_to_raw, m)?)?;
    m.add_function(wrap_pyfunction!(batch_convert_to_friendly, m)?)?;
    Ok(())
}
// src/lib.rs
use pyo3::prelude::*;
use rayon::prelude::*;
use base64::{Engine as _, engine::general_purpose::STANDARD as BASE64};

#[pyfunction]
fn batch_convert_addresses_parallel(
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
                    .map(|addr| convert_address(addr))
                    .collect()
            })
            .collect();

        Ok(results.into_iter().flatten().collect())
    })
}

fn convert_address(address: &str) -> String {
    if let Ok(decoded) = hex::decode(address.trim_start_matches("0x")) {
        // Process hex format
        format!("0:{}", hex::encode(decoded))
    } else if let Ok(decoded) = BASE64.decode(address) {
        // Process base64 format
        format!("0:{}", hex::encode(decoded))
    } else {
        // Return original if can't convert
        address.to_string()
    }
}

#[pymodule]
fn ton_address_converter(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(batch_convert_addresses_parallel, m)?)?;
    Ok(())
}
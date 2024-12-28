use base64::decode;
use ton_block::MsgAddressInt;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AddressError {
    #[error("Invalid address format")]
    InvalidFormat,
    #[error("Base64 decoding error")]
    Base64Error,
}

pub fn convert_address(address: &str) -> Result<String, AddressError> {
    // Try direct parsing first
    if let Ok(parsed) = MsgAddressInt::from_str(address) {
        return Ok(parsed.to_string());
    }
    
    // Try base64 decode if direct parsing fails
    let decoded = decode(address).map_err(|_| AddressError::Base64Error)?;
    let parsed = MsgAddressInt::construct_from_bytes(&decoded)
        .map_err(|_| AddressError::InvalidFormat)?;
    
    Ok(parsed.to_string())
}
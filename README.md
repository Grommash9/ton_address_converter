# TON Address Converter

[![PyPI Downloads](https://img.shields.io/pypi/dm/ton_address_converter.svg)](https://pypistats.org/packages/ton_address_converter)
[![Python Versions](https://img.shields.io/pypi/pyversions/ton_address_converter.svg)](https://pypi.org/project/ton_address_converter/)
[![OS Support](https://img.shields.io/badge/OS-Windows%20%7C%20macOS%20%7C%20Linux-blue.svg)](https://pypi.org/project/ton_address_converter/)

A Python library for bulk converting TON blockchain addresses between raw and user-friendly formats. Written in Rust with parallel processing capabilities, this library is particularly useful when working with large batches of addresses from block explorers or blockchain data.

## Why This Library?

When working with TON blockchain data (especially when processing blocks), addresses typically come in raw format but need to be displayed in user-friendly format for end users. This library was created to:

- Handle bulk address conversions efficiently
- Provide parallel processing for large datasets
- Maintain accuracy while optimizing performance
- Offer a simple, Pythonic API

## Performance

Our benchmarks show the following performance characteristics when compared to existing solutions:

| Number of Addresses | ton_address_converter | pytoniq | tonpy | vs pytoniq | vs tonpy |
|--------------------|----------------------|----------|--------|------------|-----------|
| 100                | 0.0018s              | 0.0006s  | 0.0001s| 0.32x      | 0.07x     |
| 1,000              | 0.0092s              | 0.0055s  | 0.0011s| 0.60x      | 0.12x     |
| 10,000             | 0.0202s              | 0.0601s  | 0.0110s| 2.98x      | 0.55x     |
| 100,000            | 0.1569s              | 0.5455s  | 0.1164s| 3.48x      | 0.74x     |

### Benchmark Environment
- intel i9 9900k
- Python 3.12.3
- pytoniq-core==0.1.40
- tonsdk==1.0.15

### Performance Analysis
- For small batches (<1,000 addresses), tonpy and pytoniq perform better due to lower overhead
- For larger batches (>10,000 addresses), ton_address_converter shows significant speedup:
  - Up to 3.48x faster than pytoniq
  - Competitive performance with tonpy
- Best suited for bulk operations where parallel processing benefits can be realized

## Installation

```bash
pip install ton_address_converter
```

## Usage

```python
from ton_address_converter import batch_convert_to_friendly, batch_convert_to_raw

# Convert raw addresses to user-friendly format
raw_addresses = [
    "0:73f17af370bd9d1f754be87a8a2d46f178aa72a9fc26f8ed9305977313f5dd29",
    # ... more addresses
]
friendly_addresses = batch_convert_to_friendly(
    raw_addresses,
    bounceable=True,    # Optional, default: False
    test_only=False,    # Optional, default: False
    url_safe=True,      # Optional, default: True
    chunk_size=1000     # Optional, default: 1000
)

# Convert friendly addresses back to raw format
raw_addresses = batch_convert_to_raw(
    friendly_addresses,
    chunk_size=1000     # Optional, default: 1000
)
```

### Common Use Cases

1. Processing block explorer data:
```python
# Convert multiple raw addresses from block data
block_addresses = [tx['address'] for tx in block_transactions]
friendly_addresses = batch_convert_to_friendly(block_addresses)
```

2. Converting user-input addresses:
```python
# Convert user-friendly addresses to raw format for blockchain operations
user_addresses = ["EQBz8XrzcL2dH3VL6HqKLUbxeKpyqfwm-O2TBZdzE_XdKTXc"]
raw_addresses = batch_convert_to_raw(user_addresses)
```

### Options

#### batch_convert_to_friendly
- `addresses`: List of raw addresses to convert
- `bounceable`: Whether to generate bounceable addresses (default: False)
- `test_only`: Whether to generate testnet addresses (default: False)
- `url_safe`: Whether to use URL-safe base64 encoding (default: True)
- `chunk_size`: Size of chunks for parallel processing (default: 1000)

#### batch_convert_to_raw
- `addresses`: List of friendly addresses to convert
- `chunk_size`: Size of chunks for parallel processing (default: 1000)

## Development

### Requirements
- Python 3.9+
- Rust (latest stable)
- maturin

### Building from source

```bash
# Clone the repository
git clone https://github.com/your_username/ton_address_converter
cd ton_address_converter

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install maturin pytest

# Build and install in development mode
maturin develop

# Run tests
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
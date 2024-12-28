from ton_address_converter import batch_convert_to_raw, batch_convert_to_friendly

# Example addresses
friendly_addresses = [
    "UQBz8XrzcL2dH3VL6HqKLUbxeKpyqfwm-O2TBZdzE_XdKWgZ",
]

raw_addresses = [
    "0:73f17af370bd9d1f754be87a8a2d46f178aa72a9fc26f8ed9305977313f5dd29",
]

# Convert friendly to raw
raw_results = batch_convert_to_raw(friendly_addresses)
print("Friendly to Raw:")
for original, converted in zip(friendly_addresses, raw_results):
    print(f"{original} -> {converted}")

# Convert raw to friendly
friendly_results = batch_convert_to_friendly(
    raw_addresses,
    bounceable=False,  # Optional, defaults to True
    # test_only=False   # Optional, defaults to False
)
print("\nRaw to Friendly:")
for original, converted in zip(raw_addresses, friendly_results):
    print(f"{original} -> {converted}")

# Bulk conversion example
large_address_list = friendly_addresses * 1000  # Create a large list
chunk_size = 100  # Optional parameter for parallel processing
bulk_results = batch_convert_to_raw(large_address_list, chunk_size=chunk_size)
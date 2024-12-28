from typing import List, Optional
from typing_extensions import TypeAlias

# Type aliases for clarity
RawAddress: TypeAlias = str
FriendlyAddress: TypeAlias = str

def batch_convert_to_raw(
    addresses: List[FriendlyAddress],
    chunk_size: Optional[int] = None
) -> List[RawAddress]: ...

def batch_convert_to_friendly(
    addresses: List[RawAddress],
    chunk_size: Optional[int] = None,
    bounceable: Optional[bool] = None,
    test_only: Optional[bool] = None,
    url_safe: Optional[bool] = None
) -> List[FriendlyAddress]: ...
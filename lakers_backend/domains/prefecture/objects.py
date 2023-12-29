from dataclasses import dataclass


@dataclass(frozen=True)
class DPrefecture:
    id: int
    name: str
    prefecture_code: str

from dataclasses import dataclass
from datetime import date


@dataclass
class ReceptionBookImportEntity:
    id: int
    prefectures_id: str
    prefectures_name: str
    import_date: date
    legal_affairs_bureau_request_month: date

from typing import Any, Dict, Final, List

from lakers_backend.domains.real_estate_book.objects import DReceptionReason
from lakers_backend.domains.real_estate_book.repositories import IReceptionReasonReader

RECEPTION_REASON_LIST: Final[List[Dict[str, Any]]] = [
    {"id": 1, "name": "所有権移転相続・法人合併"},
    {"id": 2, "name": "所有権移転遺贈・贈与その他無償名義"},
    {"id": 3, "name": "所有権移転売買"},
    {"id": 4, "name": "所有権移転その他の原因"},
    {"id": 5, "name": "権利の移転(所有権を除く)"},
    {"id": 6, "name": "処分の制限に関する登記"},
    {"id": 7, "name": "根抵当権の設定"},
    {"id": 8, "name": "抵当権の設定"},
    {"id": 9, "name": "抹消登記"},
    {"id": 10, "name": "滅失"},
    {"id": 11, "name": "建物滅失通知"},
    {"id": 12, "name": "地上権の設定"},
    {"id": 13, "name": "地役権の設定"},
    {"id": 14, "name": "賃借権の設定"},
    {"id": 15, "name": "分筆"},
    {"id": 16, "name": "合体"},
    {"id": 17, "name": "合併"},
    {"id": 18, "name": "合筆"},
    {"id": 19, "name": "所有権の保存(申請)"},
    {"id": 20, "name": "所有権の保存(職権)"},
    {"id": 21, "name": "附属建物の新築"},
    {"id": 22, "name": "敷地権たる旨の登記"},
    {"id": 23, "name": "仮登記(所有権)"},
    {"id": 24, "name": "仮登記(その他)"},
    {"id": 25, "name": "信託に関する登記"},
    {"id": 26, "name": "配偶者居住権の設定"},
    {"id": 27, "name": "買戻権"},
    {"id": 28, "name": "権利に関するその他"},
    {"id": 29, "name": "表題"},
    {"id": 30, "name": "区分建物の表題"},
    {"id": 31, "name": "敷地権の表示"},
    {"id": 32, "name": "表示に関するその他"},
    {"id": 33, "name": "登記名義人の氏名等についての変更・更正"},
    {"id": 34, "name": "権利の変更・更正"},
    {"id": 35, "name": "敷地権の表示の登記の変更・更正"},
    {"id": 36, "name": "床面積の変更・更正"},
    {"id": 37, "name": "地目変更・更正"},
    {"id": 38, "name": "地積変更・更正"},
    {"id": 39, "name": "共同担保変更通知"},
    {"id": 40, "name": "共同担保追加通知"},
    {"id": 41, "name": "分割・区分"},
    {"id": 42, "name": "却下"},
    {"id": 43, "name": "取下"},
    {"id": 999, "name": "その他"},
]


class ReceptionReasonReader(IReceptionReasonReader):
    def read(self) -> List[DReceptionReason]:
        result: List[DReceptionReason] = []
        for reception_reason in RECEPTION_REASON_LIST:
            result.append(
                DReceptionReason(
                    id=reception_reason["id"], name=reception_reason["name"]
                )
            )

        return result

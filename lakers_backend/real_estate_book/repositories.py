from typing import Dict, List

from django.db.models import Q, Subquery

from data_models.models import (
    City,
    Prefectures,
    PrefecturesCity,
    RealEstateBookType,
    RealEstateReceptionBook,
    RealEstateType,
    ReceptionBookImport,
    UserPlan,
)
from lakers_backend.domains.real_estate_book.objects import DRealEstateReceptionBook
from lakers_backend.domains.real_estate_book.repositories import (
    IRealEstateReceptionBookReader,
)
from lakers_backend.domains.reception_book_import.objects import (
    ReceptionBookImportEntity,
)
from lakers_backend.domains.reception_book_import.repositories import (
    IReceptionBookImportReader,
)
from lakers_backend.option.reception_reason.repositories import RECEPTION_REASON_LIST
from lakers_backend.utils import strtobool

from .types import RequestType


class RealEstateReceptionBookReader(IRealEstateReceptionBookReader):
    """
    DBアクセスのreadの実体
    """

    def read(
        self, user_id: int, is_superuser: bool, data: RequestType
    ) -> list[DRealEstateReceptionBook]:
        filter_condition = self.__make_filter_condition(
            user_id=user_id, is_superuser=is_superuser, data=data
        )
        exclude_condition = self.__make_exclude_condition()
        order_condition_list = self.__make_order_condition_list(data=data)
        offset = int(data["from_count"])
        limit = int(data["size"])

        real_estate_reception_books = (
            RealEstateReceptionBook.objects.select_related(
                "real_estate_book_type",
                "real_estate_type",
                "prefectures_city__prefectures",
                "prefectures_city__city",
            )
            .filter(filter_condition)
            .exclude(exclude_condition)
            .order_by(*order_condition_list)
            .all()[offset : offset + limit]
        )

        result: list[DRealEstateReceptionBook] = [
            DRealEstateReceptionBook(
                id=item.pk,
                chiban=item.chiban,
                kaoku_number=item.kaoku_number,
                real_estate_book_type_id=item.real_estate_book_type.pk
                if item.real_estate_book_type
                else None,
                real_estate_book_type_name=item.real_estate_book_type.type
                if item.real_estate_book_type
                else "",
                reception_reason=item.reception_reason,
                real_estate_type_id=item.real_estate_type.pk
                if item.real_estate_type
                else None,
                real_estate_type_name=item.real_estate_type.type
                if item.real_estate_type
                else "",
                is_new=item.is_new if item.is_new else False,
                prefectures_city_id=item.prefectures_city.pk,
                city_id=item.prefectures_city.city.pk,
                city_name=item.prefectures_city.city.name,
                prefectures_id=item.prefectures_city.prefectures.pk,
                prefectures_name=item.prefectures_city.prefectures.name,
                address=item.address,
                outside=item.outside,
                legal_affairs_bureau_request_date=item.legal_affairs_bureau_request_date,
                legal_affairs_bureau_reception_number=item.legal_affairs_bureau_reception_number,
            )
            for item in real_estate_reception_books
        ]
        return result

    def count(self, user_id: int, is_superuser: bool, data: RequestType) -> int:
        filter_condition = self.__make_filter_condition(
            user_id=user_id, is_superuser=is_superuser, data=data
        )
        return RealEstateReceptionBook.objects.filter(filter_condition).count()

    def __make_filter_condition(
        self, user_id: int, is_superuser: bool, data: RequestType
    ) -> Q:
        q_filter = Q()
        real_estate_book_type_filter = Q()
        real_estate_type_filter = Q()

        # 法務局受付日開始
        if "legal_affairs_bureau_request_date_start" in data:
            q_filter.add(
                Q(
                    legal_affairs_bureau_request_date__gte=data[
                        "legal_affairs_bureau_request_date_start"
                    ]
                ),
                Q.AND,
            )

        # 法務局受付日終了
        if "legal_affairs_bureau_request_date_end" in data:
            q_filter.add(
                Q(
                    legal_affairs_bureau_request_date__lte=data[
                        "legal_affairs_bureau_request_date_end"
                    ]
                ),
                Q.AND,
            )

        # 申請種別(単独)
        if "real_estate_book_type_tandoku" in data:
            if bool(strtobool(data["real_estate_book_type_tandoku"])):
                real_estate_book_type_filter.add(
                    Q(
                        real_estate_book_type=RealEstateBookType.objects.filter(
                            type="単独"
                        )
                        .get()
                        .pk
                    ),
                    Q.OR,
                )

        # 申請種別(連続・連先)
        if "real_estate_book_type_rensaki_renzoku" in data:
            if bool(strtobool(data["real_estate_book_type_rensaki_renzoku"])):
                real_estate_book_type_filter.add(
                    Q(
                        real_estate_book_type__in=[
                            RealEstateBookType.objects.filter(type="連続").get().pk,
                            RealEstateBookType.objects.filter(type="連先").get().pk,
                        ]
                    ),
                    Q.OR,
                )

        # 不動産種別(土地)
        if "real_estate_type_tochi" in data:
            if bool(strtobool(data["real_estate_type_tochi"])):
                real_estate_type_filter.add(
                    Q(
                        real_estate_type=RealEstateType.objects.filter(type="土地")
                        .get()
                        .pk
                    ),
                    Q.OR,
                )

        # 不動産種別(区分建物)
        if "real_estate_type_kutate" in data:
            if bool(strtobool(data["real_estate_type_kutate"])):
                real_estate_type_filter.add(
                    Q(
                        real_estate_type=RealEstateType.objects.filter(type="区分建物")
                        .get()
                        .pk
                    ),
                    Q.OR,
                )

        # 不動産種別(建物)
        if "real_estate_type_tatemono" in data:
            if bool(strtobool(data["real_estate_type_tatemono"])):
                real_estate_type_filter.add(
                    Q(
                        real_estate_type=RealEstateType.objects.filter(type="建物")
                        .get()
                        .pk
                    ),
                    Q.OR,
                )

        # 不動産種別(共担)
        if "real_estate_type_kyotan" in data:
            if bool(strtobool(data["real_estate_type_kyotan"])):
                real_estate_type_filter.add(
                    Q(
                        real_estate_type=RealEstateType.objects.filter(type="共担")
                        .get()
                        .pk
                    ),
                    Q.OR,
                )

        pref_codes_query = self.__build_prefectures_filter(
            user_id, is_superuser, data["prefectures"]
        )

        # 市区町村
        if "cities" in data:
            if len(data["cities"]) != 0:
                prefectures_cities = PrefecturesCity.objects.filter(
                    prefectures__id__in=[param.id for param in pref_codes_query],
                    city__in=City.objects.filter(id__in=data["cities"]).all(),
                )
                q_filter.add(Q(prefectures_city__in=prefectures_cities), Q.AND)
            else:
                prefectures_cities = PrefecturesCity.objects.filter(
                    prefectures__id__in=Prefectures.objects.filter(
                        pref_code__in=[param.id for param in pref_codes_query.all()]
                    ).all()
                )
                q_filter.add(Q(prefectures_city__in=prefectures_cities), Q.AND)

        # 登記原因
        selected_reception_reasons: list[str] = data["reception_reasons"]
        if len(selected_reception_reasons) != 0:
            # 選択した登記原因を検索条件に追加する
            reception_reason_filter = Q(
                reception_reason__in=[
                    reception_reason["name"]
                    for reception_reason in RECEPTION_REASON_LIST
                    if str(reception_reason["id"]) in selected_reception_reasons
                ]
            )

            # 999(その他)を含む場合、RECEPTION_REASON_LISTに存在しない登記原因を取得する
            reception_reason_other_filter = ~Q()  # ~Q()はnot表現
            if "999" in selected_reception_reasons:
                reception_reason_other_filter = ~Q(
                    reception_reason__in=[
                        record["name"]
                        for record in RECEPTION_REASON_LIST
                        if record["id"] != 999
                    ]
                )

            q_filter.add(reception_reason_other_filter | reception_reason_filter, Q.AND)

        q_filter.add(real_estate_book_type_filter, Q.AND)
        q_filter.add(real_estate_type_filter, Q.AND)

        return q_filter

    def __make_exclude_condition(self) -> Q:
        exclude_condition = (
            Q(
                # 市区町村不明を除外
                prefectures_city__city=City.objects.filter(name="不明").get()
            )
            | Q(
                # 登記原因が空白のものを除外
                reception_reason=""
            )
            | Q(
                # 登記原因が*のものを除外
                reception_reason="*"
            )
        )

        return exclude_condition

    def __build_prefectures_filter(
        self, user_id: int, is_superuser: bool, pref_codes_base: list[str]
    ):
        pref_codes = self.__build_pref_code(user_id, is_superuser, pref_codes_base)
        _filter = Q()
        for pref_code in pref_codes:
            _filter.add(Q(pref_code=pref_code), Q.OR)
        return Prefectures.objects.filter(_filter)

    @staticmethod
    def __build_pref_code(user_id: int, is_superuser: bool, pref_codes: list[str]):
        if is_superuser:
            return pref_codes or ["11", "12", "13", "14"]
        pref_city_related_plans = (
            UserPlan.objects.filter(user__id=user_id)
            .values_list(
                "plan__plan_area__prefecture_code__pref_code",
            )
            .all()
        )

        prefectures_plan = set(
            [
                prefecture_related_plan[0]
                for prefecture_related_plan in pref_city_related_plans
            ]
        )

        if len(pref_codes) > 0:
            pref_code_set = set(pref_codes) & prefectures_plan
            if len(pref_code_set) == 0:
                # 選択肢にない都道府県のみを送ってきた場合には何かしらのエラーを出力するようにする
                raise ValueError
            return pref_code_set

        return prefectures_plan

    def __make_order_condition_list(self, data: RequestType) -> List[str]:
        order_condition = [
            "legal_affairs_bureau_request_date",
            "legal_affairs_bureau_reception_number",
        ]
        if "sort_by" not in data or "order" not in data:
            return order_condition

        # ソート対象がデフォルトのOrderにある場合は削除する
        if data["sort_by"] in order_condition:
            order_condition.remove(data["sort_by"])

        # テーブル名のマッピング
        table_name_map: Dict[str, str] = {
            "prefectures": "prefectures_city__prefectures",
            "city": "prefectures_city__city",
            "reception_kind": "is_new",
        }

        # 降順だった場合はプレフィックスに-をつける
        prefix = "-" if data["order"] == "desc" else ""

        sort_by = data["sort_by"]
        if data["sort_by"] in table_name_map:
            sort_by = table_name_map[data["sort_by"]]
        order_condition.insert(0, f"{prefix}{sort_by}")

        return order_condition


class ReceptionBookImportReader(IReceptionBookImportReader):
    def read(self) -> list[ReceptionBookImportEntity]:
        # prefectureはDISTINCT ONの制約上、order_byの最初でなければNG。
        # 県別の最新を取得したあとでimport_dateの降順で取得
        items = ReceptionBookImport.objects.filter(
            pk__in=Subquery(
                ReceptionBookImport.objects.order_by("prefectures", "-import_date")
                .distinct("prefectures")
                .values("pk")
            )
        ).order_by("-import_date")

        result: list[ReceptionBookImportEntity] = [
            ReceptionBookImportEntity(
                id=item.pk,
                prefectures_id=item.prefectures.pref_code,
                prefectures_name=item.prefectures.name,
                import_date=item.import_date,
                legal_affairs_bureau_request_month=item.legal_affairs_bureau_request_month,
            )
            for item in items
        ]
        return result

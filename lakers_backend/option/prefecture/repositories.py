from data_models.models import Prefectures, UserPlan
from lakers_backend.domains.prefecture.objects import DPrefecture
from lakers_backend.domains.prefecture.repositories import IPrefectureReader


class PrefectureReader(IPrefectureReader):
    """
    DBアクセスのreadの実体
    一旦は固定値で暫定対応(後ほどちゃんとDBから取得するように回収する)
    """

    def read(self, user_id: int, is_superuser: bool) -> list[DPrefecture]:
        if is_superuser:
            return self.get_prefectures_for_superuser()
        prefecture_related_plans = self.build_filter_by_user_id(user_id).all()

        prefecture_ids = set(
            [
                prefecture_related_plan.plan.plan_area.prefecture_code.id
                for prefecture_related_plan in prefecture_related_plans
            ]
        )

        prefectures = Prefectures.objects.filter(id__in=prefecture_ids)

        return [
            DPrefecture(
                id=prefecture.id,
                prefecture_code=prefecture.pref_code,
                name=prefecture.name,
            )
            for prefecture in prefectures
        ]

    @staticmethod
    def get_prefectures_for_superuser() -> list[DPrefecture]:
        results = [
            DPrefecture(id=13, prefecture_code="13", name="東京都"),
            DPrefecture(id=14, prefecture_code="14", name="神奈川県"),
            DPrefecture(id=11, prefecture_code="11", name="埼玉県"),
            DPrefecture(id=12, prefecture_code="12", name="千葉県"),
        ]
        return results

    @staticmethod
    def build_filter_by_user_id(user_id: int):
        return UserPlan.objects.filter(user__id=user_id)

    def get_prefecture_ids(self, user_id: int) -> list[str]:
        prefecture_ids = (
            self.build_filter_by_user_id(user_id)
            .values_list(
                "plan__plan_area__prefecture_code__pref_code",
            )
            .distinct()
            .all()
        )
        return [prefecture_id[0] for prefecture_id in prefecture_ids]

    @staticmethod
    def get_prefecture_params_from_prefecture_name(pref_name: str) -> Prefectures:
        return Prefectures.objects.filter(name=pref_name).get()

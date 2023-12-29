from datetime import datetime

from data_models.models import (
    City,
    Plan,
    PlanArea,
    PlanType,
    Prefectures,
    PrefecturesCity,
    User,
    UserPlan,
)


class PrefecturesCityFactory:
    @staticmethod
    def get_or_create_prefectures() -> list[Prefectures]:
        # 次この箇所のテストを触れる際にここをtests/fixtures配下のデータを入れるようにする
        if not Prefectures.objects.filter(pref_code=13).exists():
            Prefectures.objects.create(
                id=13,
                name="東京都",
                pref_code="13",
            )
        if not Prefectures.objects.filter(pref_code=14).exists():
            Prefectures.objects.create(
                id=14,
                name="神奈川県",
                pref_code="14",
            )

        if not Prefectures.objects.filter(pref_code=11).exists():
            Prefectures.objects.create(
                id=11,
                name="埼玉県",
                pref_code="11",
            )

        if not Prefectures.objects.filter(pref_code=12).exists():
            Prefectures.objects.create(
                id=12,
                name="千葉県",
                pref_code="12",
            )

        prefectures = Prefectures.objects.filter(
            pref_code__in=["11", "12", "13", "14"]
        ).all()
        return prefectures

    @staticmethod
    def create_cities() -> list[City]:
        cities = [
            City.objects.create(name="東京都新宿区", city_code="1"),
            City.objects.create(name="横浜市青葉区", city_code="2"),
            City.objects.create(name="さいたま市大宮区", city_code="3"),
            City.objects.create(name="千葉市稲毛区", city_code="4"),
        ]
        return cities

    def create_prefectures_city(self) -> list[PrefecturesCity]:
        # 都道府県、市区町村のデータを作成する
        prefectures = self.get_or_create_prefectures()

        cities = self.create_cities()

        prefectures_cities = [
            PrefecturesCity.objects.create(prefectures=prefecture, city=city)
            for prefecture, city in zip(prefectures, cities)
        ]
        return prefectures_cities

    def create_unknown_prefectures_city(self) -> PrefecturesCity:
        # 市区町村が不明の都道府県、市区町村のデータを作成する
        prefectures = self.get_or_create_prefectures()

        city = City.objects.create(
            name="不明",
            city_code=99999,
        )

        return PrefecturesCity.objects.create(
            prefectures=prefectures[0],
            city=city,
        )

    @staticmethod
    def create_users() -> tuple[User, User, User]:
        super_user = User.objects.create_superuser("testsuper@example.com", "testsuper")
        normal_user = User.objects.create_user("test@example.com", "test")
        normal_user_only_tokyo = User.objects.create_user("test2@example.com", "test")
        return super_user, normal_user, normal_user_only_tokyo

    def create_user_and_plan(self):
        plan_type: PlanType = PlanType.objects.create(
            id=0,
            name="test",
            price=100000,
        )

        prefectures = self.get_or_create_prefectures()
        cities = self.create_cities()

        plan_areas: list[PlanArea] = []

        for index, (prefecture, city) in enumerate(zip(prefectures, cities)):
            plan_areas.append(
                PlanArea.objects.create(
                    id=index,
                    plan_name="test",
                    prefecture_code=prefecture,
                    city_code=city,
                )
            )

        plans: list[Plan] = []

        for index, plan_area in enumerate(plan_areas):
            plans.append(
                Plan.objects.create(id=index, plan_type=plan_type, plan_area=plan_area)
            )
        users = self.create_users()
        max_index = 0
        for index, plan in enumerate(plans):
            UserPlan.objects.create(
                id=index,
                plan=plan,
                user=users[1],
                contract_start_day=datetime.now(),
                contract_end_day=datetime.now(),
            )
            max_index = index + 1
        UserPlan.objects.create(
            id=max_index,
            plan=plans[0],
            user=users[2],
            contract_start_day=datetime.now(),
            contract_end_day=datetime.now(),
        )
        return users

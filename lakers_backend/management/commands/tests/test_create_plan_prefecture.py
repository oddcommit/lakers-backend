from django.core.management import call_command
from django.test import TestCase

from data_models.models import Plan
from lakers_backend.option.city.tests.factory import PrefecturesCityFactory

from .factory import PlanConfFactory


class CreatePlanPrefectureTestCase(TestCase):
    def setUp(self):
        prefectures_city_builder = PrefecturesCityFactory()
        prefectures_city_builder.create_prefectures_city()
        prefectures_city_builder.create_unknown_prefectures_city()
        self.__plan_type = PlanConfFactory.build_plan_type("東京都")

    def test__対象に結びついた都市のプランが作成されていること(self):
        call_command(
            "create_plan_prefecture",
            prefname=self.__plan_type.name,
            plantypename=self.__plan_type.name,
        )

        plans = Plan.objects.filter(plan_type__name=self.__plan_type.name).all()

        self.assertEqual(len(plans), 1)
        self.assertEqual(plans[0].plan_type, self.__plan_type)
        self.assertEqual(plans[0].plan_area.plan_name, self.__plan_type.name)
        self.assertEqual(plans[0].plan_area.prefecture_code.name, self.__plan_type.name)

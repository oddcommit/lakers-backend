from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from data_models.models import User, UserPlan
from lakers_backend.option.city.tests.factory import PrefecturesCityFactory

from .factory import PlanConfFactory


class CreateAddPlanToUserCommandTest(TestCase):
    def setUp(self):
        prefectures_city_builder = PrefecturesCityFactory()
        prefectures = prefectures_city_builder.get_or_create_prefectures()
        cities = prefectures_city_builder.create_cities()
        self.__plan_conf_factory = PlanConfFactory(prefectures, cities)
        self.__plan = self.__plan_conf_factory.build_plan("test")
        self.__user = User.objects.create_user(
            email="test@example.com", password="test@example.com"
        )

    def test__ユーザとプランが結びつけられること(self):
        call_command(
            "add_plan_to_user",
            email=self.__user.email,
            plantypename=self.__plan.plan_type.name,
            planstartdate="20230803",
        )
        user_plan = UserPlan.objects.filter(user__id=self.__user.id).first()
        self.assertIsNotNone(user_plan)
        self.assertEqual(user_plan.plan.plan_type.name, self.__plan.plan_type.name)

    def test__存在しないプランを結びつけることに失敗すること(self):
        with self.assertRaises(CommandError):
            call_command(
                "add_plan_to_user",
                email=self.__user.email,
                planname="dummy",
                planstartdate="20230803",
            )

    def test__存在しないユーザーを結びつけることに失敗すること(self):
        with self.assertRaises(CommandError):
            call_command(
                "add_plan_to_user",
                email="dummy",
                planname=self.__plan.plan_type.name,
                planstartdate="20230803",
            )

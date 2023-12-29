from django.core.management import call_command
from django.db.utils import IntegrityError
from django.test import TestCase

from data_models.models import User
from lakers_backend.option.city.tests.factory import PrefecturesCityFactory

from .factory import PlanConfFactory


class CreateUserCommandTest(TestCase):
    def setUp(self):
        prefectures_city_builder = PrefecturesCityFactory()
        prefectures = prefectures_city_builder.get_or_create_prefectures()
        cities = prefectures_city_builder.create_cities()
        self.__plan_conf_factory = PlanConfFactory(prefectures, cities)
        self.__plan_conf_factory.build_plan("test")

    def test__ユーザが作成されること(self):
        # Arrange
        email = "test@example.com"
        password = "password"
        plan = "test"
        plan_start_date = "20230803"

        # Act
        call_command(
            "create_user",
            email=email,
            password=password,
            plantypename=plan,
            planstartdate=plan_start_date,
        )

        # Assert
        user = User.objects.filter(email=email).first()
        self.assertIsNotNone(user)
        if user is not None:
            self.assertEqual(user.email, email)
            self.assertTrue(user.check_password(password))

    def test__メールアドレスが重複するユーザは作成に失敗すること(self):
        # Arrange
        email = "test@example.com"
        password = "password"
        plan = "test"
        plan_start_date = "20230803"

        User.objects.create_user(email=email, password=password)

        #  Act & Assert
        with self.assertRaises(IntegrityError):
            call_command(
                "create_user",
                email=email,
                password=password,
                plantypename=plan,
                planstartdate=plan_start_date,
            )

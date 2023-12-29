from django.test import TestCase

from lakers_backend.option.reception_reason.usecases import ReceptionReasonUsecase


class ReceptionReasonUsecaseTest(TestCase):
    def setUp(self):
        self.use_case = ReceptionReasonUsecase()

    def test__feed__戻り値の型にlistが含まれていること(self):
        # Act
        actual = self.use_case.feed()

        # Assert
        self.assertIn("list", actual)

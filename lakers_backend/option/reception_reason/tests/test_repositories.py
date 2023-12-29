from django.test import TestCase

from lakers_backend.option.reception_reason.repositories import ReceptionReasonReader


class ReceptionReasonReaderTest(TestCase):
    def setUp(self):
        self.repository = ReceptionReasonReader()

    def test__read__定義した登記原因のリストが取得できること(self):
        # Act
        actual = self.repository.read()

        # Assert
        self.assertEqual(len(actual), 44)

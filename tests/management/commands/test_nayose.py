from django.test import TestCase

from lakers_backend.management.commands.util.nayose import convert_ascii


class NayoseTest(TestCase):
    def test__ひらがなは半角にならない数字および記号は半角になる(self):
        converted_result = convert_ascii("大田区南久が原２丁目２-３")
        self.assertEqual(converted_result, "大田区南久が原2丁目2-3")

    def test__数値が入ってきた場合はnanになる(self):
        converted_result = convert_ascii(1.0)
        self.assertEqual(converted_result, "nan")

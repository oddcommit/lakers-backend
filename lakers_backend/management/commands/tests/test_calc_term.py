from datetime import datetime

from django.test import TestCase

from lakers_backend.management.commands.util.calc_term import calc_term


class CreateCalcTermTest(TestCase):
    def test__閏年の1月31に日プラン登録した場合の１ヶ月プランの末尾は2月29日(self):
        start_date_str = "20240131"
        start_date, end_date = calc_term(start_date_str, 1)
        february_29 = "20240229"
        self.assertEqual(start_date, datetime.strptime(start_date_str, "%Y%m%d"))
        self.assertEqual(end_date, datetime.strptime(february_29, "%Y%m%d"))

    def test__閏年ではない年の1月31に日プラン登録した場合の１ヶ月プランの末尾は2月29日(self):
        start_date_str = "20230131"
        start_date, end_date = calc_term(start_date_str, 1)
        february_29 = "20230228"
        self.assertEqual(start_date, datetime.strptime(start_date_str, "%Y%m%d"))
        self.assertEqual(end_date, datetime.strptime(february_29, "%Y%m%d"))

    def test__閏年の前の年の12月31に日プラン登録した場合の3ヶ月プランの末尾は2月29日(self):
        start_date_str = "20231130"
        start_date, end_date = calc_term(start_date_str)
        february_28 = "20240229"
        self.assertEqual(start_date, datetime.strptime(start_date_str, "%Y%m%d"))
        self.assertEqual(end_date, datetime.strptime(february_28, "%Y%m%d"))

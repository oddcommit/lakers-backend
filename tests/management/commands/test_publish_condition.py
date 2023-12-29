from django.test import TestCase

from lakers_backend.management.commands.util.publish_condition import (
    build_publish_conditions,
    calc_publish_plug,
)


class PublishConditionTest(TestCase):
    def test__生の文言から公開条件のインデックスを取得できる(self):
        result = calc_publish_plug("１．オープンデータ公開可")
        self.assertEqual(result, 1)

    def test__生の文言がnanの場合公開なしのインデックスになる(self):
        result = calc_publish_plug(float("nan"))
        self.assertEqual(result, 4)

    def test__公開フラグが1なら空の配列を返す(self):
        result = build_publish_conditions(1, "１．有償利用不可、２．再配信不可")
        self.assertEqual(result, [])

    def test__公開フラグが1なら条件が付与されていても空の配列を返す(self):
        result = build_publish_conditions(1, "１．有償利用不可、２．再配信不可")
        self.assertEqual(result, [])

    def test__公開条件を表す文字列から公開条件のインデックスを抽出できる(self):
        result = build_publish_conditions(2, "１．有償利用不可、２．再配信不可")
        self.assertEqual(result, [1, 2])

    def test__公開条件が記述されていない場合公開されていないインデックスの4を返す(self):
        result = build_publish_conditions(4, float("nan"))
        self.assertEqual(result, [4])

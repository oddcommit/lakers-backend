from django.test import TestCase

from ..data_input.load_chiseki_map import load_dataloader, load_geojson, load_jsonl


class LoadChisekiTest(TestCase):
    def test__jsonlで呼び出されるように指定するとjsonlで読み込み関数が呼ばれる(self):
        result = load_dataloader(True)
        self.assertEqual(result, load_jsonl)

    def test__jsonl意外で呼び出されるように指定するとjsonで読み込み関数が呼ばれる(self):
        result = load_dataloader(False)
        self.assertEqual(result, load_geojson)

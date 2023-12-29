# Test用データ置き場

[conftest.py](..%2Fconftest.py) から下記のデータが読み込まれます。

- [master_datas.jsonl](master_datas.jsonl): 住所系のマスターデータ
- [code_datas.jsonl](code_datas.jsonl): 物件タイプ等のコード系


## 参考）TableデータをDumpする方法

```sh
poetry run python manage.py dumpdata data_models.City --format jsonl -o tests/fixtures/city.jsonl
```

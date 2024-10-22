# Generated by Django 4.2 on 2023-09-05 05:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data_models", "0037_alter_realestatereceptionbook_kaoku_number"),
    ]

    operations = [
        migrations.CreateModel(
            name="Building",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "kaoku_number",
                    models.CharField(blank=True, max_length=256, verbose_name="家屋番号"),
                ),
                (
                    "real_estate_id",
                    models.CharField(max_length=256, null=True, verbose_name="不動産ID"),
                ),
                (
                    "owner_latest_get_date",
                    models.DateField(null=True, verbose_name="所有者事項最新取得日"),
                ),
                ("latitude", models.FloatField(verbose_name="代表点緯度:土地と紐づくまでの暫定")),
                ("longitude", models.FloatField(verbose_name="代表点緯度:土地と紐づくまでの暫定")),
            ],
        ),
        migrations.AddField(
            model_name="realestatereceptionbook",
            name="land",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="data_models.land",
                verbose_name="土地データ",
            ),
        ),
        migrations.AddIndex(
            model_name="land",
            index=models.Index(
                fields=["prefecture_city", "chiban"],
                name="data_models_prefect_0b6976_idx",
            ),
        ),
        migrations.AddField(
            model_name="building",
            name="land",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="data_models.land",
                verbose_name="土地ID",
            ),
        ),
        migrations.AddField(
            model_name="building",
            name="prefecture_city",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="data_models.prefecturescity",
                verbose_name="市区町村都道府県ID",
            ),
        ),
        migrations.AddField(
            model_name="building",
            name="real_estate_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="data_models.realestatetype",
                verbose_name="不動産タイプID",
            ),
        ),
        migrations.AddField(
            model_name="realestatereceptionbook",
            name="building",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="data_models.building",
                verbose_name="建物データ",
            ),
        ),
        migrations.AddIndex(
            model_name="building",
            index=models.Index(
                fields=["prefecture_city", "kaoku_number"],
                name="data_models_prefect_b0f9f5_idx",
            ),
        ),
    ]

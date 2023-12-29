# Generated by Django 4.2 on 2023-09-05 07:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data_models", "0038_building_realestatereceptionbook_land_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="BuildingAreaUsePurpose",
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
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="登録日時"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新日時"),
                ),
                (
                    "area_use_purpose",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="data_models.areausepurpose",
                        verbose_name="用途地域データ",
                    ),
                ),
                (
                    "building",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="data_models.building",
                        verbose_name="土地データ",
                    ),
                ),
            ],
        ),
    ]
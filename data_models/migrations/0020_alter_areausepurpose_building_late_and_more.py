# Generated by Django 4.2 on 2023-08-24 06:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data_models", "0019_areausepurpose"),
    ]

    operations = [
        migrations.AlterField(
            model_name="areausepurpose",
            name="building_late",
            field=models.FloatField(verbose_name="建ぺい率"),
        ),
        migrations.AlterField(
            model_name="areausepurposeconditions",
            name="publish_flag",
            field=models.IntegerField(
                choices=[(1, "公開データ"), (2, "条件付き公開データ"), (3, "非公開データ")],
                verbose_name="公開条件",
            ),
        ),
    ]

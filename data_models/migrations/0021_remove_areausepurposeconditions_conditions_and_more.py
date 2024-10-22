# Generated by Django 4.2 on 2023-08-24 08:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data_models", "0020_alter_areausepurpose_building_late_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="areausepurposeconditions",
            name="conditions",
        ),
        migrations.AlterField(
            model_name="areausepurposeconditions",
            name="publish_flag",
            field=models.IntegerField(
                choices=[(1, "公開データ"), (2, "条件付き公開データ"), (3, "非公開データ"), (4, "回答なし")],
                verbose_name="公開可否",
            ),
        ),
    ]

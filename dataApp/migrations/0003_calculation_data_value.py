# Generated by Django 4.2.1 on 2023-05-11 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dataApp", "0002_alter_calculation_health_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="calculation",
            name="data_value",
            field=models.CharField(default=None, max_length=30),
            preserve_default=False,
        ),
    ]

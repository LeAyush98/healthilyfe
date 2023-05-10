# Generated by Django 4.2.1 on 2023-05-10 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dataApp", "0003_alter_healthdata_date_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="healthdata",
            name="health_data",
            field=models.CharField(
                choices=[
                    ("blood pressure", "Blood Pressure"),
                    ("height weight", "Height/Weight in m/Kg"),
                    ("heart rate", "Heart Rate in bpm"),
                ],
                max_length=30,
            ),
        ),
    ]

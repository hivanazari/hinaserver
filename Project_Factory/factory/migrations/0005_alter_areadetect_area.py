# Generated by Django 4.1.5 on 2023-02-05 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("factory", "0004_areadetect"),
    ]

    operations = [
        migrations.AlterField(
            model_name="areadetect",
            name="area",
            field=models.CharField(max_length=50, verbose_name="ناحیه"),
        ),
    ]

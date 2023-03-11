# Generated by Django 4.1.5 on 2023-01-24 10:43

from django.db import migrations, models
import django.db.models.deletion
import factory.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CameraModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='نام دوربین')),
            ],
            options={
                'verbose_name': ' نام دوربین ',
                'verbose_name_plural': ' نام دوربین ',
            },
        ),
        migrations.CreateModel(
            name='FactoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام کارخانه')),
                ('address', models.TextField(verbose_name='آدرس')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='شماره تماس')),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='factory.cameramodel', verbose_name='نام دوربین')),
            ],
            options={
                'verbose_name': 'نام کارخانه',
                'verbose_name_plural': 'نام کارخانه',
            },
        ),
        migrations.CreateModel(
            name='FactoryImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factory_image', models.ImageField(upload_to=factory.models.Profile_image_path, verbose_name='عکس پلاک')),
                ('Warnings', models.CharField(blank=True, max_length=225, verbose_name='هشدار')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')),
                ('factory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='factory.factorymodel', verbose_name='نام دوربین')),
            ],
            options={
                'verbose_name': 'شماره پلاک',
                'verbose_name_plural': 'شماره پلاک',
            },
        ),
    ]

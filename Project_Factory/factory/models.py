from django.db import models
import os
from django.conf import settings
from django.utils.html import mark_safe
# Create your models here.
import datetime


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def Profile_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.pk}-{name}{ext}"
    x = f"Image/{final_name}"
    return x


class AreaModel(models.Model):
    area = models.CharField(max_length=60, verbose_name='ناحیه')

    def __str__(self):
        return f'{self.area}'

    class Meta:
        verbose_name = ("ناحیه")
        verbose_name_plural = ("ناحیه")


class CameraModel(models.Model):
    name = models.CharField(max_length=60, verbose_name='نام دوربین')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = (" دوربین ")
        verbose_name_plural = (" دوربین ")


class CategoryModel(models.Model):
    tilte = models.CharField(max_length=60, verbose_name='نوع')

    def __str__(self):
        return f'{self.tilte}'

    class Meta:
        verbose_name = ("نوع")
        verbose_name_plural = ("نوع")


class FactoryModel(models.Model):
    camera = models.ForeignKey(
        CameraModel, on_delete=models.CASCADE, verbose_name='نام دوربین')
    factory_name = models.CharField(max_length=100, verbose_name='نام کارخانه')
    address = models.TextField(verbose_name='آدرس', null=True, blank=True)
    phone = models.CharField(max_length=11, unique=True,
                             blank=False, null=False, verbose_name='شماره تماس')

    def __str__(self):
        return f'{self.factory_name}'

    class Meta:
        verbose_name = ('کارخانه')
        verbose_name_plural = ('کارخانه')


def mainproductFile(instance, filename):
    dateti = str(datetime.datetime.now().year)+"_" + \
        str(datetime.datetime.now().month)+"_"+str(datetime.datetime.now().day)
    return '/'.join([dateti, str(instance.area), "main", str(instance.time_read)+".jpg"])


class AreaDetect(models.Model):
    area = models.CharField(verbose_name="ناحیه", max_length=50)
    category = models.CharField(verbose_name="نام شی", max_length=50)
    warning = models.BooleanField(verbose_name="هشدار")
    xyxy = models.CharField(verbose_name="مختصات ها", max_length=255)
    date_read = models.DateField(verbose_name="تاریخ تشخیص")
    main_image = models.ImageField(
        blank=True, verbose_name="تصویر ", upload_to=mainproductFile)

    time_read = models.TimeField(verbose_name="زمان قرائت", auto_now=False)

    class Meta:
        verbose_name = "تشخیص ها"


class FactoryImageModel(models.Model):
    factory = models.ForeignKey(
        FactoryModel, on_delete=models.CASCADE, verbose_name='کارخانه')
    factory_image = models.ImageField(
        upload_to=Profile_image_path, verbose_name='عکس وسیله یا شخص')
    category = models.ForeignKey(
        CategoryModel, on_delete=models.CASCADE, verbose_name='نوع')
    area = models.ForeignKey(
        AreaModel, on_delete=models.CASCADE, verbose_name='ناحیه')
    Warnings = models.TextField(blank=True, verbose_name='هشدار')
    date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')

    def __str__(self):
        return f'{self.factory.factory_name}'

    class Meta:
        verbose_name = ("عکس کارخانه")
        verbose_name_plural = ("عکس کارخانه")

    def image(self):
        if self.factory_image != '':
            return mark_safe('<img src="%s%s" width="45" height="45" />' % (f'{settings.MEDIA_URL}', self.factory_image))

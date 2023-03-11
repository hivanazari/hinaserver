from django.contrib import admin
from .models import *
# Register your models here.


class FactoryImageAdmin(admin.ModelAdmin):
    readonly_fields=('date', )
    list_display = ['pk','Warnings', 'image', 'date', 'category', 'area']
    search_fields = ['factory']
    list_filter = ['factory', 'date']
class AreaDetectAdmin(admin.ModelAdmin):
   
    list_display = ['pk', 'warning', 'main_image', 'date_read', 'category','area']
    # search_fields = ['area']
    # list_filter = ['area', 'date']
admin.site.register(AreaDetect,AreaDetectAdmin)
admin.site.register(AreaModel)
admin.site.register(CameraModel)
admin.site.register(CategoryModel)
admin.site.register(FactoryModel)
admin.site.register(FactoryImageModel, FactoryImageAdmin)
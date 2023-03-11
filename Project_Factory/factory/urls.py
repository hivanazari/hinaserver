from django.urls import path
from .views import *


urlpatterns = [
    path('detect', dectect_list, name='پایش'),
    path('area', area, name='منطقه'),
    path('camera', camera, name='دوربین'),
    path('category', category, name='نوع ابجکت'),
    path('factory', factory, name='کارخانه'),
    path('factory_image', factory_image, name='عکس کارخانه'),
]
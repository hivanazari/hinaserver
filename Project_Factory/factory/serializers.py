from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import *
class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension
class AreaDetectSeializer(serializers.ModelSerializer):
 
    main_image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model=AreaDetect
        fields=('area','category','warning','xyxy','date_read','time_read','main_image')
class AreaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= AreaModel
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model= CategoryModel
        fields = '__all__'


class CameraSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= CameraModel
        fields = '__all__'

class FactorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model= FactoryModel
        fields = '__all__'

class FactoryImageSerializer(serializers.ModelSerializer):
    factory_image = Base64ImageField()

    class Meta:
        model= FactoryImageModel
        fields = '__all__'
        # depth = 1

    def create(self, validated_data):
        return FactoryImageModel.objects.create(**validated_data)



class FactoryImageSerializer2(serializers.ModelSerializer):

    class Meta:
        model= FactoryImageModel
        fields = '__all__'
        depth = 2
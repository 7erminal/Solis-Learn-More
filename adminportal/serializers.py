from rest_framework import serializers
from adminportal.models import VideoLog
    

class VideoUploadSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    videoFile = serializers.FileField()
    category = serializers.IntegerField()
    language = serializers.IntegerField()
    timestamp = serializers.IntegerField(required=False)

class CategorySerializer(serializers.Serializer):
    categoryName = serializers.CharField(max_length=100)
    categoryDescription = serializers.CharField()

class CategorySerializerGet(serializers.Serializer):
    categoryId = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=200)

class CategoryResponseSerializer(serializers.Serializer):
    StatusCode = serializers.IntegerField()
    StatusDesc = serializers.CharField()
    Result = CategorySerializerGet()

class CategoriesResponseSerializer(serializers.Serializer):
    StatusCode = serializers.IntegerField()
    StatusDesc = serializers.CharField()
    Result = CategorySerializerGet(many=True)

class LanguageSerializer(serializers.Serializer):
    languageName = serializers.CharField(max_length=100)
    languageCode = serializers.CharField(max_length=10)

class LanguageSerializerGet(serializers.Serializer):
    languageId = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    code = serializers.CharField(max_length=10)

class LanguageResponseSerializer(serializers.Serializer):
    StatusCode = serializers.IntegerField()
    StatusDesc = serializers.CharField()
    Result = LanguageSerializerGet()

class LanguagesResponseSerializer(serializers.Serializer):
    StatusCode = serializers.IntegerField()
    StatusDesc = serializers.CharField()
    Result = LanguageSerializerGet(many=True)

class VideoUploadSerializerList(serializers.ModelSerializer):
    # category = CategorySerializerGet()
    # language = LanguageSerializerGet()
    videoFile = serializers.CharField()
    class Meta:
        model = VideoLog
        fields = '__all__'
        depth = 1

class VideoUploadResponseSerializer(serializers.Serializer):
    StatusCode = serializers.IntegerField()
    StatusDesc = serializers.CharField()
    Result = VideoUploadSerializerList()

class VideosUploadResponseSerializer(serializers.Serializer):
    StatusCode = serializers.IntegerField()
    StatusDesc = serializers.CharField()
    Result = VideoUploadSerializerList(many=True)
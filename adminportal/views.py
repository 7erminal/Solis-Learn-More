from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
from adminportal.serializers import CategoriesResponseSerializer, LanguagesResponseSerializer, VideoUploadSerializer, VideoUploadSerializerList, LanguageSerializer, CategorySerializer, LanguageSerializerGet, CategorySerializerGet, VideoUploadResponseSerializer, CategoryResponseSerializer, LanguageResponseSerializer, VideosUploadResponseSerializer
from adminportal.models import VideoLog, Language, Category

import logging
logger = logging.getLogger("django")

class Resp:
	def __init__(self, StatusDesc, Result, StatusCode):
		self.StatusDesc=StatusDesc
		self.Result=Result
		self.StatusCode=StatusCode

class VideoUploadView(viewsets.ViewSet):
    def create(self, request):
        serializer = VideoUploadSerializer(data=request.data)
        message = "Video uploaded successfully"
        status_ = status.HTTP_200_OK
        if serializer.is_valid():
            # Process the validated data here
            videoFile = serializer.validated_data.get('videoFile')
            title = serializer.validated_data.get('title')
            description = serializer.validated_data.get('description')
            category = serializer.validated_data.get('category')
            language = serializer.validated_data.get('language')
            logger.info("Uploading video file: %s", videoFile.name)
            logger.info("Title: %s", title)
            logger.info("Description: %s", description)
            # Save the video file
            video = VideoLog.objects.create(
                title=title,
                description=description,
                videoFile=videoFile,
                category=Category.objects.get(pk=category),
                language=Language.objects.get(pk=language)
            )

            video.save()
            resp = Resp(StatusDesc=message, StatusCode=status_, Result=VideoUploadSerializerList(video).data)
            return Response(VideoUploadResponseSerializer(resp).data, status=status.HTTP_201_CREATED)
        else:
            logger.error("Video upload failed: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        queryset = VideoLog.objects.all()
        message = "Videos retrieved successfully"
        status_ = status.HTTP_200_OK
        logger.info("Retrieved videos: %s", queryset)

        serializer = VideoUploadSerializerList(queryset, many=True)
        logger.info("Serialized videos: %s", serializer.data)
        resp = Resp(StatusDesc=message, StatusCode=status_, Result=serializer.data)
        logger.info("Response prepared: %s", VideosUploadResponseSerializer(resp).data)
        return Response(VideosUploadResponseSerializer(resp).data, status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        try:
            video = VideoLog.objects.get(pk=pk)
            serializer = VideoUploadSerializerList(video)
            message = "Video retrieved successfully"
            status_ = status.HTTP_200_OK

            logger.info("Video retrieved: %s", serializer.data)
            resp = Resp(StatusDesc=message, StatusCode=status_, Result=serializer)
            return Response(VideoUploadResponseSerializer(resp).data, status.HTTP_200_OK)
        except VideoLog.DoesNotExist:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        try:
            video = VideoLog.objects.get(pk=pk)
            video.delete()
            return Response({"message": "Video deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except VideoLog.DoesNotExist:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk=None):
        try:
            video = VideoLog.objects.get(pk=pk)
            serializer = VideoUploadSerializer(data=request.data)
            message = "Video updated successfully"
            status_ = status.HTTP_200_OK
            if serializer.is_valid():
                video.title = serializer.validated_data.get('title', video.title)
                video.description = serializer.validated_data.get('description', video.description)
                videoFile = serializer.validated_data.get('videoFile', None)
                if videoFile:
                    video.videoFile = videoFile
                video.save()
                resp = Resp(StatusDesc=message, StatusCode=status_, Result=VideoUploadSerializerList(video).data)
                return Response(VideoUploadResponseSerializer(resp).data, status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except VideoLog.DoesNotExist:
            message = "Video not found"
            status_ = status.HTTP_404_NOT_FOUND
            resp = Resp(StatusDesc=message, StatusCode=status_, Result={})
            return Response(VideoUploadResponseSerializer(resp).data, status=status.HTTP_404_NOT_FOUND)
        

class LanguageViewSet(viewsets.ViewSet):
    def list(self, request):
        # Logic to list languages
        message = "Languages retrieved successfully"
        status_ = status.HTTP_200_OK
        try:
            languages = Language.objects.all()
            logger.info("Retrieved languages: %s", languages)
            serializer = LanguageSerializerGet(languages, many=True).data
            logger.info("Serialized languages: %s", serializer)
            resp = Resp(StatusDesc=message, StatusCode=status_, Result=serializer)
            return Response(LanguagesResponseSerializer(resp).data, status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error retrieving languages: %s", str(e))
            return Response({"error": "Error retrieving languages"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        # Logic to create a new language
        message = "Language created successfully"
        status_ = status.HTTP_201_CREATED
        serializer = LanguageSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('languageName')
            code = serializer.validated_data.get('languageCode')
            language = Language.objects.create(
                name=name,
                code=code
            )
            language.save()
            resp = Resp(StatusDesc=message, StatusCode=status_, Result=LanguageSerializerGet(language).data)
            return Response(LanguageResponseSerializer(resp).data, status=status.HTTP_201_CREATED)
        else:
            logger.error("Language creation failed: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        try:
            message = "Language retrieved successfully"
            status_ = status.HTTP_200_OK
            language = Language.objects.get(pk=pk)
            serializer = LanguageSerializerGet(language)
            resp = Resp(StatusDesc=message, StatusCode=status_, Result=serializer)
            return Response(LanguageResponseSerializer(resp).data, status.HTTP_200_OK)
        except Language.DoesNotExist:
            return Response({"error": "Language not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        try:
            language = Language.objects.get(pk=pk)
            language.delete()
            return Response({"message": "Language deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Language.DoesNotExist:
            return Response({"error": "Language not found"}, status=status.HTTP_404_NOT_FOUND)

class CategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        # Logic to list categories
        message = "Categories retrieved successfully"
        status_ = status.HTTP_200_OK
        try:
            categories = Category.objects.all()
            logger.info("Retrieved categories: %s", categories)
            serializer = CategorySerializerGet(categories, many=True).data
            logger.info("Serialized categories: %s", serializer)
            resp = Resp(StatusDesc=message, StatusCode=status_, Result=serializer)
            return Response(CategoriesResponseSerializer(resp).data, status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error retrieving categories: %s", str(e))
            return Response({"error": "Error retrieving categories"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        # Logic to create a new category
        message = "Category created successfully"
        status_ = status.HTTP_200_OK
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('categoryName')
            description = serializer.validated_data.get('categoryDescription')
            category = Category.objects.create(
                name=name,
                description=description
            )
            category.save()
            resp = Resp(StatusDesc=message, StatusCode=status_, Result=CategorySerializerGet(category).data)
            return Response(CategoryResponseSerializer(resp).data, status=status.HTTP_201_CREATED)
        else:
            logger.error("Category creation failed: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        message = "Category retrieved successfully"
        status_ = status.HTTP_200_OK
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializerGet(category)
            resp = Resp(StatusDesc=message, StatusCode=status_, Result=serializer)
            return Response(CategoryResponseSerializer(resp).data, status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
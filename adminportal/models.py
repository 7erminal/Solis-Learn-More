from django.db import models

# Create your models here.
class Category(models.Model):
    categoryId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

class Language(models.Model):
    languageId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

class VideoLog(models.Model):
    videoLogId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='video_log_category')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='video_log_language')
    videoFile = models.FileField(upload_to='video-logs', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
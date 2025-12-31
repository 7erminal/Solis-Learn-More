from django.urls import include, path
from rest_framework import routers

from adminportal import views

router = routers.DefaultRouter()
router.register(r'videos', views.VideoUploadView, basename='video')
router.register(r'languages', views.LanguageViewSet, basename='language')
router.register(r'categories', views.CategoryViewSet, basename='category')

urlpatterns = [
    path('portal/', include(router.urls)),
    # path('portal/videos/', views.VideoUploadView.as_view({'get': 'list', 'post': 'create'}), name='video-list'),
    # path('portal/languages/', views.LanguageViewSet.as_view({'get': 'list', 'post': 'create'}), name='language-list'),
    # path('portal/categories/', views.CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
# 
]
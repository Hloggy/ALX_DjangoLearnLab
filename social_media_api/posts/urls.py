from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]


Include the posts URLs in your main urls.py:

python
from django.urls import path, include

urlpatterns = [
    # ... other URLs
    path('api/', include('posts.urls')),
]


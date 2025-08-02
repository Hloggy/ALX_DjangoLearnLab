from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet  # Make sure these match your view classes

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),
]

from django.urls import path
from .views import BookListView, BookCreateView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    # Add other endpoints as needed
]

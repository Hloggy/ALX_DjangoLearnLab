from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Filtering options
    filterset_fields = {
        'title': ['exact', 'icontains'],
        'author': ['exact', 'icontains'],
        'publication_year': ['exact', 'gte', 'lte'],
    }
    
    # Searching options
    search_fields = ['title', 'author', 'description']
    
    # Ordering options
    ordering_fields = ['title', 'author', 'publication_year', 'price']
    ordering = ['title']  # Default ordering

from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

# BookList view (from Task 1)
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# BookViewSet (from Task 2)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly

class BookListView(generics.ListAPIView):
    """
    View to list all books (GET)
    Accessible to all users (authenticated or not)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to view

class BookDetailView(generics.RetrieveAPIView):
    """
    View to retrieve a single book by ID (GET)
    Accessible to all users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class BookCreateView(generics.CreateAPIView):
    """
    View to create a new book (POST)
    Restricted to authenticated users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Automatically set the current user as the book's owner"""
        serializer.save(added_by=self.request.user)

    def create(self, request, *args, **kwargs):
        """Customize the response format"""
        response = super().create(request, *args, **kwargs)
        # Add custom response data
        response.data = {
            'status': 'success',
            'data': response.data,
            'message': 'Book created successfully',
            'created_at': timezone.now().isoformat()
        }
        return response

class BookUpdateView(generics.UpdateAPIView):
    """
    View to update an existing book (PUT/PATCH)
    Restricted to authenticated users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly]

class BookDeleteView(generics.DestroyAPIView):
    """
    View to delete a book (DELETE)
    Restricted to authenticated users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly]


from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from .permissions import IsOwnerOrReadOnly  # Custom permission

class BookListView(generics.ListAPIView):
    """
    View to list all books (GET)
    Public access (no authentication required)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class BookCreateView(generics.CreateAPIView):
    """
    View to create a new book (POST)
    Requires authentication
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the creator to the current user
        serializer.save(created_by=self.request.user)

class BookDetailView(generics.RetrieveAPIView):
    """
    View to retrieve a single book (GET)
    Public access
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class BookUpdateView(generics.UpdateAPIView):
    """
    View to update a book (PUT/PATCH)
    Requires authentication and ownership
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class BookDeleteView(generics.DestroyAPIView):
    """
    View to delete a book (DELETE)
    Requires authentication and ownership
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"status": "success", "message": "Book deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

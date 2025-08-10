from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book, Author

class BookAPITest(APITestCase):

    def setUp(self):
        # Create a test user and log in
        self.user = User.objects.create_user(username='maud', password='mypassword')
        self.client.login(username='maud', password='mypassword')

        # Create an author
        self.author = Author.objects.create(name="Chimamanda Ngozi")

        # Create a book linked to the author
        self.book = Book.objects.create(
            title="Purple Hibiscus",
            author=self.author,
            publication_year=2002
        )

        # URLs based on your urls.py naming (make sure to update if different)
        self.list_url = reverse('book-list')           # List view URL name
        self.create_url = reverse('book-create')       # Create view URL name
        self.detail_url = reverse('book-detail', args=[self.book.id])  # Detail view URL name
        self.update_url = reverse('book-update', args=[self.book.id])  # Update view URL name
        self.delete_url = reverse('book-delete', args=[self.book.id])  # Delete view URL name

    def test_create_book(self):
        data = {
            'title': 'New Book',
            'author': self.author.id,
            'publication_year': 2020
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(response.data['title'], 'New Book')

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # We only created one book in setUp

    def test_detail_book(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    def test_update_book(self):
        data = {
            'title': 'Updated Title',
            'author': self.author.id,
            'publication_year': 2005
        }
        response = self.client.put(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')

    def test_delete_book(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

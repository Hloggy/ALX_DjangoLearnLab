from django.db import models

class Author(models.Model):
    """
    Represents an author who writes books.
    Fields:
        name: The name of the author (CharField)
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Represents a book written by an author.
    Fields:
        title: The title of the book (CharField)
        publication_year: The year the book was published (IntegerField)
        author: ForeignKey relationship to Author model (one-to-many)
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title




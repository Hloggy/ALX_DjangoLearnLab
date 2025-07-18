from bookshelf.models import Book
#Create Book
book = Book.objects.create(title="The gods are not to blame", author="Ola Rotimi",publication_year=2005)
#output:
<Book: Book object (4)>
#Retrieve Book
Book.objects.get(title="1984")
#Update Book
book.title = “Nineteen Eighty-Four”
book.save()
#Delete Book
book.delete()
#output:
(1, {'bookshelf.Book': 1})

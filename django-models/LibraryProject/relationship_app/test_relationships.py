from relationship_app.models import Author, Book, Library, Librarian

# Create Author objects
chinua = Author.objects.create(name="Chinua Achebe")
ama = Author.objects.create(name="Ama Ata Aidoo")
other_author = Author.objects.create(name="Author Name")

# Create Book objects and assign to authors
things = Book.objects.create(title="Things Fall Apart", author=chinua)
dilemma = Book.objects.create(title="Dilemma of a Ghost", author=ama)

# Query books by author
books_by_ama = Book.objects.filter(author=ama)
books_by_chinua = Book.objects.filter(author=chinua)

# List all books
all_books = Book.objects.all()

# Create Library instance
balme = Library.objects.create(name='Balme Library')

# Add books to the library
balme.books.add(things, dilemma)

# List all books in the library
books_in_balme = balme.books.all()

# Add Librarian to the library
agyim = Librarian.objects.create(name='Agyim Taala', library=balme)

# Retrieve the librarian for the library
librarian_for_balme = Librarian.objects.get(library=balme)

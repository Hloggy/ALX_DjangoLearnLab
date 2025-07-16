# Admin Interface for Book Model

- Registered the Book model with Django admin using @admin.register(Book)
- Customized the admin with:
  - list_display for title, author, publication_year
  - list_filter for author and year
  - search_fields for title and author
- Created a superuser and confirmed the model shows up in /admin/

from django.shortcuts import render
from .models import Book, Author

# Create your views here.
def list_books(request):
    books = Book.objects.all()
    return render(request, "books.html", {'books': books})

def create_book(request):
    author = Author.objects.get(id=1)
    Book.objects.create(name="Book 1", pub_date="2025-01-01", authors=author)

def list_authors(request):
    authors = Author.objects.all()
    return render(request, "authors.html", {'authors': authors})

def create_author(request):
    books = Book.objects.all()
    Author.objects.create(name="Author 1", books=books)
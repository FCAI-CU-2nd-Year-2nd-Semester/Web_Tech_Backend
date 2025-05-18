from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import os
from datetime import datetime

def book_cover_path(instance, filename):
    # Get current date
    now = datetime.now()
    # Create path: books/covers/%y/%m/%d/filename
    return os.path.join('books', 'covers', now.strftime('%y'), now.strftime('%m'), now.strftime('%d'), filename)

def book_pdf_path(instance, filename):
    # Get current date
    now = datetime.now()
    # Create path: books/pdfs/%y/%m/%d/filename
    return os.path.join('books', 'pdfs', now.strftime('%y'), now.strftime('%m'), now.strftime('%d'), filename)

class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='authors/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cover_image = models.ImageField(upload_to=book_cover_path)
    pdf_file = models.FileField(upload_to=book_pdf_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'book')
    
    def __str__(self):
        return f"{self.user.username}'s cart - {self.book.title}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')
        
    def __str__(self):
        return f"{self.user.username}'s favorite - {self.book.title}"

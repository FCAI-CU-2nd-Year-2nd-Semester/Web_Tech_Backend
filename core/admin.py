from django.contrib import admin
from .models import Author, Book, CartItem, Favorite

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio')
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'discount_price', 'is_available')
    list_filter = ('author', 'is_available')
    search_fields = ('title', 'author__name')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('price', 'discount_price', 'is_available')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'quantity', 'added_at')
    list_filter = ('user',)
    search_fields = ('user__username', 'book__title')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'book')
    list_filter = ('user',)
    search_fields = ('user__username', 'book__title')

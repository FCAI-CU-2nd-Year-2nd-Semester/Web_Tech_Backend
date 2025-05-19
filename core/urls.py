from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('send-code/', views.send_code_view, name='send_code'),
    path('resend-code/', views.resend_code_view, name='resend_code'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('my-cart/', views.my_cart_view, name='my_cart'),
    path('favourites/', views.favourites_view, name='favourites'),
    path('book/<int:book_id>/', views.book_details_view, name='book_details'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('add-favorite/', views.add_favorite, name='add_favorite'),
    path('remove-favorite/', views.remove_favorite, name='remove_favorite'),
    path('books/', views.books_view, name='books'),
]
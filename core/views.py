from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Book, Favorite, CartItem

# Create your views here.

@login_required(login_url='login')
def index(request):
    books = Book.objects.all()
    return render(request, 'pages/index.html', {'books': books})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('index')
        messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'pages/Login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserCreationForm()
    return render(request, 'pages/SignUp.html', {'form': form})

def forgot_password_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        # Here you would typically:
        # 1. Check if email exists
        # 2. Generate a verification code
        # 3. Send the code via email
        # For now, we'll just redirect to send code page
        messages.success(request, 'Verification code has been sent to your email.')
        return redirect('send_code')
    return render(request, 'pages/ForgetPassword.html')

def send_code_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        # Here you would typically:
        # 1. Verify the code
        # 2. If valid, redirect to change password
        # For now, we'll just redirect to change password
        return redirect('change_password')
    return render(request, 'pages/Send_Code.html')

def change_password_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        if new_password1 != new_password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'pages/ChangePassword.html')
            
        # Here you would typically:
        # 1. Validate password strength
        # 2. Update the user's password
        # 3. Redirect to login
        messages.success(request, 'Password changed successfully! Please login with your new password.')
        return redirect('login')
    return render(request, 'pages/ChangePassword.html')

@login_required(login_url='login')
def my_cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.book.price * item.quantity for item in cart_items)
    return render(request, 'pages/MyCart.html', {
        'cart_items': cart_items,
        'total': total,
        'is_empty': not cart_items.exists()
    })

@login_required(login_url='login')
def favourites_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('book')
    return render(request, 'pages/Favourites.html', {
        'favorite_items': favorites,
        'favorites': favorites,
        'is_empty': not favorites.exists()
    })

@login_required(login_url='login')
def book_details_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    is_favorite = Favorite.objects.filter(user=request.user, book=book).exists()
    in_cart = CartItem.objects.filter(user=request.user, book=book).exists()
    return render(request, 'pages/book-details.html', {
        'book': book,
        'is_favorite': is_favorite,
        'in_cart': in_cart,
        'cart_count': CartItem.objects.filter(user=request.user).count(),
        'favorite_count': Favorite.objects.filter(user=request.user).count()
    })

@login_required
@require_POST
def add_to_cart(request):
    book_id = request.POST.get('book_id')
    quantity = int(request.POST.get('quantity', 1))
    book = Book.objects.get(id=book_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, book=book)
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        cart_item.quantity = quantity
        cart_item.save()
    return JsonResponse({'success': True, 'cart_count': CartItem.objects.filter(user=request.user).count()})

@login_required
@require_POST
def remove_from_cart(request):
    book_id = request.POST.get('book_id')
    CartItem.objects.filter(user=request.user, book_id=book_id).delete()
    return JsonResponse({'success': True, 'cart_count': CartItem.objects.filter(user=request.user).count()})

@login_required
@require_POST
def add_favorite(request):
    book_id = request.POST.get('book_id')
    book = Book.objects.get(id=book_id)
    Favorite.objects.get_or_create(user=request.user, book=book)
    return JsonResponse({'success': True, 'favorite_count': Favorite.objects.filter(user=request.user).count()})

@login_required
@require_POST
def remove_favorite(request):
    book_id = request.POST.get('book_id')
    Favorite.objects.filter(user=request.user, book_id=book_id).delete()
    return JsonResponse({'success': True, 'favorite_count': Favorite.objects.filter(user=request.user).count()})

# These functions are duplicates of my_cart_view and favourites_view
# They are kept for reference but not used in the URLs

def newbooks_view(request):
    books = Book.objects.filter(is_available=True)
    return render(request, 'pages/newbooks.html', {'books': books})

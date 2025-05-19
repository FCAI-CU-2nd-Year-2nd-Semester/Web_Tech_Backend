from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Book, Favorite, CartItem
from django.contrib.auth.models import User
import random
import string
from django.core.mail import send_mail
from django.conf import settings

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
        
        
        # Check if user with this email exists
        try:
            user = User.objects.get(email=email)
            
            
            # Generate a random 6-digit code
            verification_code = ''.join(random.choices(string.digits, k=6))
            
            # Store the verification code in session
            request.session['reset_code'] = verification_code
            request.session['reset_user_id'] = user.id
            request.session['reset_email'] = user.email
            
            print(f"Session updated: reset_code={verification_code}, reset_user_id={user.id}, reset_email={user.email}")
            
            # Send verification email
            subject = 'Password Reset Verification Code'
            message = f'Your verification code is: {verification_code}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            
            try:
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, 'Verification code has been sent to your email.')
                
                # Print to console for debugging
                print(f"EMAIL SENT TO: {email}")
                print(f"SUBJECT: {subject}")
                print(f"MESSAGE: {message}")
                print("==========================\n")
                
                return redirect('send_code')
            except Exception as e:
                messages.error(request, f'Failed to send verification code. Error: {str(e)}')
                
        except User.DoesNotExist:
            messages.success(request, 'If your email exists in our system, a verification code has been sent.')
            return redirect('send_code')
            
    return render(request, 'pages/ForgetPassword.html')

@require_POST
def resend_code_view(request):
    """Handle resending verification code via AJAX"""
    user_id = request.session.get('reset_user_id')
    email = request.session.get('reset_email')
    

    
    if not user_id or not email:
        return JsonResponse({
            'success': False,
            'message': 'Your session has expired. Please restart the password reset process.'
        })
    
    try:
        # Generate a new verification code
        verification_code = ''.join(random.choices(string.digits, k=6))
        
        # Update the session with the new code
        request.session['reset_code'] = verification_code
        
        # Send new verification email
        subject = 'Password Reset Verification Code'
        message = f'Your new verification code is: {verification_code}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        
        # Debug email info
        print(f"\nRESENDING EMAIL TO: {email}")
        print(f"SUBJECT: {subject}")
        print(f"MESSAGE: {message}")
        
        send_mail(subject, message, from_email, recipient_list)
        
        return JsonResponse({
            'success': True,
            'message': 'New verification code sent successfully.'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Failed to send verification code: {str(e)}'
        })

def send_code_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        # Combine all code inputs to form the complete code
        submitted_code = ''
        for i in range(1, 7):
            submitted_code += request.POST.get(f'code{i}', '')
            
        # Get stored verification code from session
        stored_code = request.session.get('reset_code')
        
        if submitted_code == stored_code:
            messages.success(request, 'Code verified successfully.')
            return redirect('change_password')
        else:
            messages.error(request, 'Invalid verification code. Please try again.')
            
    return render(request, 'pages/Send_Code.html')

def change_password_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    # Check if we have a user_id in session
    user_id = request.session.get('reset_user_id')
    
    
    if not user_id:
        messages.error(request, 'Password reset session has expired. Please start over.')
        return redirect('forgot_password')
        
    if request.method == 'POST':
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        # Validate password
        if new_password1 != new_password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'pages/ChangePassword.html')
        
        if len(new_password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'pages/ChangePassword.html')
            
        # Additional password strength validation (optional)
        has_uppercase = any(c.isupper() for c in new_password1)
        has_lowercase = any(c.islower() for c in new_password1)
        has_digit = any(c.isdigit() for c in new_password1)
        has_special = any(not c.isalnum() for c in new_password1)
        
        if not (has_uppercase and has_lowercase and has_digit and has_special):
            messages.error(request, 'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character.')
            return render(request, 'pages/ChangePassword.html')
        
        try:
            user = User.objects.get(id=user_id)
            
            # Set the new password
            user.set_password(new_password1)
            user.save()
            messages.success(request, 'Password changed successfully. You can now log in with your new password.')            
            # Clean up session
            if 'reset_code' in request.session:
                del request.session['reset_code']
            if 'reset_user_id' in request.session:
                del request.session['reset_user_id']
            if 'reset_email' in request.session:
                del request.session['reset_email']
            
            
            messages.success(request, 'Your password has been changed successfully. Please log in with your new password.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'User not found. Please try again.')
            return redirect('forgot_password')
            
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

@login_required(login_url='login')
def books_view(request):
    books = Book.objects.all()
    return render(request, 'pages/books.html', {'books': books})

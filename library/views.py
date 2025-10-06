from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Book, Profile
from .forms import BookForm, RegisterForm, ProfileForm


def index(request):
    """Homepage view."""
    return render(request, 'library/index.html')


@login_required
def dashboard(request):
    """Dashboard view showing user's books with statistics."""
    status_filter = request.GET.get('status', None)
    
    if status_filter:
        books = Book.objects.filter(user=request.user, status=status_filter)
    else:
        books = Book.objects.filter(user=request.user)
    
    # Calculate statistics
    total_books = Book.objects.filter(user=request.user).count()
    completed_books = Book.objects.filter(user=request.user, status='Completed').count()
    reading_books = Book.objects.filter(user=request.user, status='Reading').count()
    planned_books = Book.objects.filter(user=request.user, status='Planned').count()
    
    # Calculate completion percentage
    completion_percentage = (completed_books / total_books * 100) if total_books > 0 else 0
    
    context = {
        'books': books,
        'total_books': total_books,
        'completed_books': completed_books,
        'reading_books': reading_books,
        'planned_books': planned_books,
        'completion_percentage': round(completion_percentage, 1),
        'status_filter': status_filter,
    }
    
    return render(request, 'library/dashboard.html', context)


@login_required
def add_book(request):
    """Add a new book view."""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('dashboard')
    else:
        form = BookForm()
    
    return render(request, 'library/add.html', {'form': form})


@login_required
@require_http_methods(["POST"])
def update_book(request, book_id):
    """Update book status via AJAX."""
    book = get_object_or_404(Book, id=book_id, user=request.user)
    
    new_status = request.POST.get('status')
    if new_status in ['Reading', 'Completed', 'Planned']:
        book.status = new_status
        book.save()
        return JsonResponse({
            'success': True,
            'message': f'Book status updated to {new_status}',
            'new_status': new_status
        })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid status'
    }, status=400)


@login_required
@require_http_methods(["POST"])
def delete_book(request, book_id):
    """Delete a book via AJAX."""
    book = get_object_or_404(Book, id=book_id, user=request.user)
    book_title = book.title
    book.delete()
    
    return JsonResponse({
        'success': True,
        'message': f'Book "{book_title}" deleted successfully'
    })


def register_view(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, 'library/register.html', {'form': form})


def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Welcome back, {username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'library/login.html', {'form': form})


def logout_view(request):
    """User logout view."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('index')


@login_required
def profile_view(request):
    """User profile view."""
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'library/profile.html', {'form': form})


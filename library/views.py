from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Book, Profile
from .forms import BookForm, RegisterForm, ProfileForm
import json
import requests


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


# ==================== AI Tools Views ====================

def ai_tools_view(request):
    """AI Tools page view."""
    return render(request, 'library/ai_tools.html')


@require_http_methods(["POST"])
def ai_summarize(request):
    """
    AI Book Summarizer endpoint.
    Accepts text and returns a concise AI-generated summary.
    """
    try:
        # Parse JSON request body
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        
        if not text:
            return JsonResponse({
                'success': False,
                'error': 'Please provide text to summarize.'
            }, status=400)
        
        # Check if API key is configured
        if not settings.OPENAI_API_KEY:
            return JsonResponse({
                'success': False,
                'error': 'OpenAI API key not configured. Please add OPENAI_API_KEY to your .env file.'
            }, status=500)
        
        # Call OpenAI API using direct HTTP requests
        headers = {
            'Authorization': f'Bearer {settings.OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a helpful assistant that creates concise, clear summaries of text passages. Focus on the main ideas and key points.'
                },
                {
                    'role': 'user',
                    'content': f'Please provide a concise summary of the following text:\n\n{text}'
                }
            ],
            'max_tokens': 300,
            'temperature': 0.7
        }
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            summary = result['choices'][0]['message']['content'].strip()
            
            return JsonResponse({
                'success': True,
                'summary': summary
            })
        else:
            error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            return JsonResponse({
                'success': False,
                'error': f'OpenAI API error: {error_msg}'
            }, status=500)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data.'
        }, status=400)
    
    except requests.exceptions.Timeout:
        return JsonResponse({
            'success': False,
            'error': 'Request timeout. Please try again.'
        }, status=500)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }, status=500)


@require_http_methods(["POST"])
def ai_recommend(request):
    """
    AI Book Recommender endpoint.
    Accepts a topic and returns AI-generated book recommendations.
    """
    try:
        # Parse JSON request body
        data = json.loads(request.body)
        topic = data.get('topic', '').strip()
        
        if not topic:
            return JsonResponse({
                'success': False,
                'error': 'Please provide a topic or interest.'
            }, status=400)
        
        # Check if API key is configured
        if not settings.OPENAI_API_KEY:
            return JsonResponse({
                'success': False,
                'error': 'OpenAI API key not configured. Please add OPENAI_API_KEY to your .env file.'
            }, status=500)
        
        # Call OpenAI API using direct HTTP requests
        headers = {
            'Authorization': f'Bearer {settings.OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a knowledgeable book recommendation assistant. Provide exactly 5 book recommendations. For each book, provide: 1) Title, 2) Author, 3) Brief description (2-3 sentences). Format each book on separate lines like this:\n\n1. [Title] by [Author]\n[Description]\n\n2. [Title] by [Author]\n[Description]'
                },
                {
                    'role': 'user',
                    'content': f'Recommend 5 books about: {topic}. Please format each recommendation clearly with title, author, and description.'
                }
            ],
            'max_tokens': 1000,
            'temperature': 0.8
        }
        
        api_response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if api_response.status_code != 200:
            error_msg = api_response.json().get('error', {}).get('message', 'Unknown error')
            return JsonResponse({
                'success': False,
                'error': f'OpenAI API error: {error_msg}'
            }, status=500)
        
        # Parse the AI response
        result = api_response.json()
        ai_response = result['choices'][0]['message']['content'].strip()
        
        # Parse text response into structured data
        recommendations = []
        lines = ai_response.split('\n')
        current_book = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if it's a new book entry (starts with number)
            if line and line[0].isdigit() and ('. ' in line or ') ' in line):
                # Save previous book if exists
                if current_book and 'title' in current_book and 'author' in current_book:
                    recommendations.append(current_book)
                
                # Start new book
                current_book = {}
                
                # Extract title and author from line like "1. Title by Author"
                # Remove the number prefix
                text = line.split('.', 1)[1].strip() if '.' in line else line.split(')', 1)[1].strip()
                
                if ' by ' in text.lower():
                    # Split by "by" (case insensitive)
                    parts = text.lower().split(' by ')
                    title_part = text[:text.lower().index(' by ')].strip()
                    author_part = text[text.lower().index(' by ') + 4:].strip()
                    
                    # Remove any trailing dashes or special chars
                    title_part = title_part.rstrip(' -–—')
                    author_part = author_part.split('\n')[0].strip()  # Only first line
                    
                    current_book['title'] = title_part
                    current_book['author'] = author_part
                    current_book['description'] = ''
                else:
                    # No author found in title line
                    current_book['title'] = text
                    current_book['author'] = 'Various Authors'
                    current_book['description'] = ''
            elif current_book and 'title' in current_book:
                # Add to description
                if line.lower().startswith('by '):
                    # Found author on separate line
                    if not current_book.get('author') or current_book['author'] == 'Various Authors':
                        current_book['author'] = line[3:].strip()
                else:
                    # Add to description
                    if current_book['description']:
                        current_book['description'] += ' ' + line
                    else:
                        current_book['description'] = line
        
        # Don't forget the last book
        if current_book and 'title' in current_book and 'author' in current_book:
            recommendations.append(current_book)
        
        # Ensure all books have proper fields
        for book in recommendations:
            if not book.get('author'):
                book['author'] = 'Various Authors'
            if not book.get('description'):
                book['description'] = 'A highly recommended book in this genre.'
            # Clean up descriptions
            book['description'] = book['description'].strip()
        
        # Ensure we have at least some recommendations
        if not recommendations:
            recommendations = [
                {'title': f'Best Books about {topic}', 'author': 'Various Authors', 'description': 'Explore popular titles in this genre at your local library or bookstore.'},
                {'title': f'{topic}: An Introduction', 'author': 'Various Authors', 'description': 'A great starting point for readers interested in this topic.'},
                {'title': f'Classic {topic} Literature', 'author': 'Various Authors', 'description': 'Timeless works that have shaped this genre.'}
            ]
        
        # Limit to 5 recommendations
        recommendations = recommendations[:5]
        
        return JsonResponse({
            'success': True,
            'recommendations': recommendations
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data.'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }, status=500)


@require_http_methods(["POST"])
def ai_quiz(request):
    """
    AI Quiz Generator endpoint.
    Accepts book title, author, and difficulty level, returns AI-generated quiz questions.
    """
    try:
        # Parse JSON request body
        data = json.loads(request.body)
        title = data.get('title', '').strip()
        author = data.get('author', '').strip()
        difficulty = data.get('difficulty', '').strip()
        
        if not title or not author or not difficulty:
            return JsonResponse({
                'success': False,
                'error': 'Please provide book title, author, and difficulty level.'
            }, status=400)
        
        # Check if API key is configured
        if not settings.OPENAI_API_KEY:
            return JsonResponse({
                'success': False,
                'error': 'OpenAI API key not configured. Please add OPENAI_API_KEY to your .env file.'
            }, status=500)
        
        # Call OpenAI API using direct HTTP requests
        headers = {
            'Authorization': f'Bearer {settings.OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {
                    'role': 'system',
                    'content': f'You are a quiz generator. Create {difficulty.lower()} level quiz questions about books. Provide exactly 5 questions with their answers. Format your response as a JSON array with objects containing "question" and "answer" fields.'
                },
                {
                    'role': 'user',
                    'content': f'Generate 5 {difficulty.lower()} level quiz questions about the book "{title}" by {author}. Include the answers.'
                }
            ],
            'max_tokens': 1000,
            'temperature': 0.7
        }
        
        api_response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if api_response.status_code != 200:
            error_msg = api_response.json().get('error', {}).get('message', 'Unknown error')
            return JsonResponse({
                'success': False,
                'error': f'OpenAI API error: {error_msg}'
            }, status=500)
        
        # Parse the AI response
        result = api_response.json()
        ai_response = result['choices'][0]['message']['content'].strip()
        
        # Try to parse as JSON, if it fails, create a structured response
        try:
            questions = json.loads(ai_response)
        except:
            # Fallback: parse text response into structured data
            questions = []
            lines = ai_response.split('\n')
            current_question = {}
            
            for line in lines:
                line = line.strip()
                if line.startswith(('Q', '1.', '2.', '3.', '4.', '5.', 'Question')):
                    if current_question and 'question' in current_question:
                        questions.append(current_question)
                    current_question = {}
                    # Extract question
                    q_text = line.lstrip('Q0123456789.:Question ').strip()
                    current_question['question'] = q_text
                elif line.startswith(('A', 'Answer')) and current_question:
                    # Extract answer
                    a_text = line.lstrip('A:Answer ').strip()
                    current_question['answer'] = a_text
            
            if current_question and 'question' in current_question:
                questions.append(current_question)
            
            # Ensure all questions have answers
            for q in questions:
                if 'answer' not in q:
                    q['answer'] = 'Answer not provided.'
        
        # Ensure exactly 5 questions
        questions = questions[:5]
        
        # Pad with generic questions if less than 5
        while len(questions) < 5:
            questions.append({
                'question': f'Question {len(questions) + 1} about {title}',
                'answer': 'Please refer to the book for details.'
            })
        
        return JsonResponse({
            'success': True,
            'questions': questions
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data.'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }, status=500)


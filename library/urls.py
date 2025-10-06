from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_book, name='add_book'),
    path('update/<int:book_id>/', views.update_book, name='update_book'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('auth/register/', views.register_view, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # AI Tools routes
    path('ai/', views.ai_tools_view, name='ai_tools'),
    path('ai/summarize/', views.ai_summarize, name='ai_summarize'),
    path('ai/recommend/', views.ai_recommend, name='ai_recommend'),
    path('ai/quiz/', views.ai_quiz, name='ai_quiz'),
]


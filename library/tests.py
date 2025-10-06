from django.test import TestCase
from django.contrib.auth.models import User
from .models import Book, Profile


class BookModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            status='Reading',
            user=self.user
        )
    
    def test_book_creation(self):
        self.assertEqual(self.book.title, 'Test Book')
        self.assertEqual(self.book.author, 'Test Author')
        self.assertEqual(self.book.status, 'Reading')
        self.assertEqual(self.book.user, self.user)
    
    def test_book_str(self):
        self.assertEqual(str(self.book), 'Test Book by Test Author')


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
    
    def test_profile_auto_creation(self):
        # Profile should be automatically created
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, Profile)
    
    def test_profile_str(self):
        self.assertEqual(str(self.user.profile), "testuser's profile")


class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
    
    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library/index.html')
    
    def test_dashboard_requires_login(self):
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)  # Redirects to login
    
    def test_dashboard_with_login(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library/dashboard.html')


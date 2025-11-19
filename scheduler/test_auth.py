from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class AuthenticationTest(TestCase):
    """Test authentication functionality."""
    
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(
            username='existinguser',
            password='existingpass123',
            email='existing@example.com'
        )
    
    def test_signup_page_loads(self):
        """Test that signup page loads successfully."""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign Up')
    
    def test_signup_with_valid_data(self):
        """Test user registration with valid data."""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'New',
            'last_name': 'User'
        })
        
        # Should redirect to dashboard after successful signup
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
        
        # Verify user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        new_user = User.objects.get(username='newuser')
        self.assertEqual(new_user.email, 'newuser@example.com')
        self.assertEqual(new_user.first_name, 'New')
        self.assertEqual(new_user.last_name, 'User')
    
    def test_signup_with_mismatched_passwords(self):
        """Test signup fails with mismatched passwords."""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'differentpass123'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'password')
        self.assertFalse(User.objects.filter(username='newuser').exists())
    
    def test_login_page_loads(self):
        """Test that login page loads successfully."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')
    
    def test_login_with_correct_credentials(self):
        """Test login with correct credentials."""
        response = self.client.post(reverse('login'), {
            'username': 'existinguser',
            'password': 'existingpass123'
        })
        
        # Should redirect to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
        
        # Verify user is logged in
        user = User.objects.get(username='existinguser')
        self.assertTrue(self.client.session.get('_auth_user_id'))
    
    def test_login_with_incorrect_credentials(self):
        """Test login with incorrect credentials."""
        response = self.client.post(reverse('login'), {
            'username': 'existinguser',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'username and password')
        self.assertFalse(self.client.session.get('_auth_user_id'))
    
    def test_logout(self):
        """Test logout functionality."""
        # First login
        self.client.login(username='existinguser', password='existingpass123')
        self.assertTrue(self.client.session.get('_auth_user_id'))
        
        # Then logout
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        
        # Verify user is logged out
        self.assertFalse(self.client.session.get('_auth_user_id'))
    
    def test_authenticated_user_redirected_from_signup(self):
        """Test that logged-in users are redirected from signup page."""
        self.client.login(username='existinguser', password='existingpass123')
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
    
    def test_protected_views_require_login(self):
        """Test that protected views require authentication."""
        # Test dashboard
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
        
        # Test create meeting
        response = self.client.get(reverse('create_meeting'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

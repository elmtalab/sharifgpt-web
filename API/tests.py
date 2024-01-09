from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from .models import CustomUser

class UserTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user('testuser', password='12345')

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': '12345'})
        self.assertRedirects(response, '/dashboard.html')

    def test_register(self):
        response = self.client.post(reverse('register'), {'username': 'newuser', 'password1': '12345', 'password2': '12345', 'email': 'newuser@example.com'})
        self.assertRedirects(response, '/dashboard.html')

    # Add more tests as needed

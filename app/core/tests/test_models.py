from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        username = 'testuser'
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for idx, (email, expected) in enumerate(sample_emails):
            user = get_user_model().objects.create_user(username=f'testuser{idx}', email=email, password='sample123')
            self.assertEqual(user.email, expected)
    
    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(username='testuser', email='', password='test123')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'testuser', 'test@example.com', 'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

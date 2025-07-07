# Create your tests here.
"""
Test suite for Users API endpoints.

To run tests:
    python manage.py test users
"""
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterTests(APITestCase):
    def test_register_success(self):
        url = '/api/auth/register/'
        data = {
            "name": "New User",
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpassword"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['username'], 'newuser')

    def test_register_missing_field(self):
        url = '/api/auth/register/'
        data = {"username": "nouser", "email": "no@example.com"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])

class LoginTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testlogin', email='login@example.com', name='Test Login', password='pass1234'
        )
        self.url = '/api/auth/login/'

    def test_login_success(self):
        data = {"username": "testlogin", "password": "pass1234"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('access', response.data['data'])

    def test_login_failure(self):
        data = {"username": "testlogin", "password": "wrongpass"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['success'])

class UserDetailTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='detailuser', email='detail@example.com', name='Detail User', password='detailpass'
        )
        login = self.client.post(
            '/api/auth/login/',
            {"username": "detailuser", "password": "detailpass"},
            format='json'
        )
        token = login.data['data']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_get_user(self):
        response = self.client.get('/api/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['username'], 'detailuser')

    def test_update_user(self):
        new_data = {"name": "Updated Name", "email": "updated@example.com"}
        response = self.client.put('/api/user/update/', new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Updated Name')

    def test_reset_password(self):
        data = {"old_password": "detailpass", "new_password": "newdetailpass"}
        response = self.client.post('/api/user/reset-password/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password('newdetailpass'))

    def test_delete_user(self):
        response = self.client.delete('/api/user/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username='detailuser').exists())

class CheckUsernamesTests(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='existsuser', email='ex@example.com', name='Exists', password='pass1234'
        )
        self.url = '/api/user/check-usernames/'

    def test_check_usernames(self):
        data = {"usernames": ["existsuser", "freeuser"]}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['available'], ['freeuser'])

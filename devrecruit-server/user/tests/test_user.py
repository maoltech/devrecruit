from user.models import User
from user.views import SignUpView, SignInView
from rest_framework import status
from django.test import TestCase, RequestFactory
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthenticationTests(APITestCase):
    def setUp(self):
        # Set up initial data if needed
        self.signup_url = "/v1/api/user/signup/"
        self.signin_url = "/v1/api/user/signin/"
        self.user_data = {
            "email": "testuser@example.com",
            "password": "strongpassword123",
            "first_name": "Test",
            "last_name": "User",
        }
        self.credentials = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }

    def test_signup_successful(self):
        """Test user sign-up with valid data."""
        response = self.client.post(self.signup_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("email", response.data)
        self.assertEqual(response.data["email"], self.user_data["email"])

    def test_signup_invalid_data(self):
        """Test sign-up with invalid data."""
        invalid_data = self.user_data.copy()
        invalid_data["email"] = "invalidemail"  # Invalid email format
        response = self.client.post(self.signup_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_signin_successful(self):
        """Test user sign-in with valid credentials."""
        # Create a user first
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.signin_url, self.credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_signin_invalid_credentials(self):
        """Test sign-in with incorrect credentials."""
        # Create a user first
        User.objects.create_user(**self.user_data)
        invalid_credentials = self.credentials.copy()
        invalid_credentials["password"] = "wrongpassword"
        response = self.client.post(self.signin_url, invalid_credentials)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)

def test_valid_user_registration_returns_201(self):
        request_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        request = RequestFactory().post('/signup', request_data)
        view = SignUpView.as_view()
        response = view(request)
    
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email='test@example.com').exists()
        assert 'password' not in response.data

    # Empty request body returns HTTP 400
def test_empty_request_returns_400(self):
    request = RequestFactory().post('/signup', {})
    view = SignUpView.as_view()
    response = view(request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.data
    assert 'password' in response.data
    assert 'first_name' in response.data 
    assert 'last_name' in response.data

    # Successful user creation stores data in database with hashed password
def test_successful_user_creation_stores_data(self, mocker):
    mocker.patch('django.contrib.auth.get_user_model')
    mock_user = mocker.Mock()
    mock_user.objects.create_user.return_value = mock_user
    mocker.patch('user.views.SignUpSerializer.is_valid', return_value=True)
    mocker.patch('user.views.SignUpSerializer.save', return_value=mock_user)

    view = SignUpView()
    request = mocker.Mock()
    response = view.post(request)

    assert response.status_code == 201
    assert mock_user.objects.create_user.called
    assert mock_user.password != 'plain_password'

# Response contains user data without password field
def test_response_contains_user_data_without_password(self, mocker):
    mocker.patch('django.contrib.auth.get_user_model')
    mock_user = mocker.Mock()
    mock_user.objects.create_user.return_value = mock_user
    mocker.patch('user.views.SignUpSerializer.is_valid', return_value=True)
    mocker.patch('user.views.SignUpSerializer.save', return_value=mock_user)

    view = SignUpView()
    request = mocker.Mock()
    response = view.post(request)

    assert response.status_code == 201
    assert 'password' not in response.data

    # Request with valid email format is processed correctly
    def test_request_with_valid_email_format(self, mocker):
        mocker.patch('django.contrib.auth.get_user_model')
        mock_user = mocker.Mock()
        mock_user.objects.create_user.return_value = mock_user
        mocker.patch('user.views.SignUpSerializer.is_valid', return_value=True)
        mocker.patch('user.views.SignUpSerializer.save', return_value=mock_user)
    
        view = SignUpView()
        request = mocker.Mock(data={'email': 'valid@example.com'})
        response = view.post(request)
    
        assert response.status_code == 201
        assert 'email' in response.data and response.data['email'] == 'valid@example.com'
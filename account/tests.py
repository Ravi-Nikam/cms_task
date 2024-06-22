from .models import CustomUser as User, Post, Like
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class UserTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.token = self.get_token_for_user(self.user)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_create_user(self):
        url = reverse('create-account')
        data = {"email": "ravinikam@gmail.com","name": "ravi nikam","phone": "9876543212","date_of_birth": "1998-09-12","gender": "M","password":"ravinikam"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_user(self):
        url = reverse('MyProfileView')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_update_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        url = reverse('user-detail', args=[self.user.id])
        data = {"name": "jamkudi","phone": "1234567890","date_of_birth": "1898-09-23","gender": "F"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'jamkudi')
        self.assertEqual(self.user.phone, '1234567890')

    def test_delete_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)
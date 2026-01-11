from unittest.mock import patch
from rest_framework.test import APITestCase
from rest_framework import status
from .models import SpyCat

class SpyCatTests(APITestCase):
    @patch('cats.serializers.validate_breed')
    def test_create_cat_valid_breed(self, mock_validate):
        mock_validate.return_value = True
        data = {
            "name": "Milo",
            "years_of_experience": 5,
            "breed": "British Shorthair",
            "salary": "500.00"
        }
        response = self.client.post('/api/cats/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SpyCat.objects.count(), 1)
        self.assertEqual(SpyCat.objects.get().name, 'Milo')

    @patch('cats.serializers.validate_breed')
    def test_create_cat_invalid_breed(self, mock_validate):
        mock_validate.return_value = False
        data = {
            "name": "Invalid",
            "years_of_experience": 1,
            "breed": "Dog",
            "salary": "100.00"
        }
        response = self.client.post('/api/cats/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

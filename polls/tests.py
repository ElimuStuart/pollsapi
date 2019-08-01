from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

from polls import apiviews


class TestPoll(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.view = apiviews.PollViewSet.as_view({'get': 'list'})
        self.uri = '/polls/'
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='test@example.com',
            password='test'
        )

    def test_list(self):
        request = self.factory.get(self.uri, HTTP_AUTHORIZATION='Token {0}'.format(self.token.key))
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200, 'Expected code: 200 received {0} instead.'.format(response.status_code))

    def test_list2(self):
        self.client.login(username="test", password="test")
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200, 'Expected code: 200 received {0} instead.'.format(response.status_code))

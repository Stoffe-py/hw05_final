from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from posts.models import Post


class PaginatorViewsTest(TestCase):
    AUTH_USER = 'TestName'
    POST_TEXT = 'Тестовый текст'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = get_user_model().objects.create(username=cls.AUTH_USER)

        Post.objects.bulk_create([Post(text=f'{cls.POST_TEXT}{i}',
                                       author=cls.user)
                                  for i in range(13)])

    def test_first_page_containse_ten_records(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_page_containse_three_records(self):
        response = self.client.get(reverse('index') + '?page=2')
        self.assertEqual(len(response.context.get('page').object_list), 3)

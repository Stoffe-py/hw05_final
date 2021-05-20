from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Post, Group


class PostsURLTests(TestCase):
    AUTH_USER = 'testname1'
    GROUP_TITLE = 'Тестовое название группы'
    GROUP_SLUG = 'test-slug'
    GROUP_DSCRPTN = 'Тестовое описание группы'
    POST_TEXT = 'Тестовый текст поста'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = get_user_model().objects.create(
            username=cls.AUTH_USER)
        # Создадим запись в БД для проверки доступности адреса group/test-slug/
        cls.group = Group.objects.create(title=cls.GROUP_TITLE,
                                         slug=cls.GROUP_SLUG,
                                         description=cls.GROUP_DSCRPTN,
                                         )

        cls.post = Post.objects.create(text=cls.POST_TEXT,
                                       author=cls.user,
                                       group=cls.group,
                                       )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.reverse_name_index = reverse('index')
        self.reverse_name_group = reverse('group_posts',
                                          kwargs={'slug': self.GROUP_SLUG})
        self.reverse_name_new_post = reverse('post_new')
        self.reverse_name_profile = reverse('profile',
                                            kwargs={
                                                'username': self.AUTH_USER})
        self.reverse_name_post_view = reverse('post', kwargs={
                                              'username': self.AUTH_USER,
                                              'post_id': self.post.pk})

    def test_urls_authorized_client(self):
        status_list = {
            self.reverse_name_index: 200,
            self.reverse_name_group: 200,
            self.reverse_name_new_post: 200,
            self.reverse_name_profile: 200,
            self.reverse_name_post_view: 200,
        }

        for url_name, status_code in status_list.items():
            with self.subTest(url=url_name):
                response = self.authorized_client.get(url_name)
                self.assertEqual(status_code, response.status_code)

    # 6 спринт страницы с ошибками
    def test_server_return_404_if_page_not_found(self):
        response = self.authorized_client.get('/notrealpage/')
        self.assertEqual(response.status_code, 404)

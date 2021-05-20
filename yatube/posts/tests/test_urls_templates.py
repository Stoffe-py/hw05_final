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
        self.reverse_name_profile = reverse('profile',
                                            kwargs={
                                                'username': self.AUTH_USER})
        self.reverse_name_post_view = reverse('post', kwargs={
                                              'username': self.AUTH_USER,
                                              'post_id': self.post.pk})

        self.reverse_name_post_edit = reverse('post_edit', kwargs={
                                              'username': self.AUTH_USER,
                                              'post_id': self.post.pk})

    def test_all_templates(self):
        templates_list = {
            'index.html': '/',
            'group.html': '/group/test-slug/',
            'new.html': '/new/',
            'profile.html': self.reverse_name_profile,
            'post.html': self.reverse_name_post_view,
            'post_edit.html': self.reverse_name_post_edit,
        }

        for template, reverse_name in templates_list.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

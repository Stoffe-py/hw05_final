from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group


class NewPostFormTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # создаем авторизованного пользователя
        cls.user = get_user_model().objects.create(username='TestName')
        cls.group = Group.objects.create(
            title='Тестовое название',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.authorized_user = Client()
        cls.authorized_user.force_login(cls.user)

    def test_create_post(self):
        """Тестирование формы создания поста."""
        # Подсчитаем количество записей в Post
        posts_count = Post.objects.count()
        # Подготавливаем данные для передачи в форму
        form_data = {
            'group': self.group.id,
            'text': 'Тестовый текст',
        }
        response = self.authorized_user.post(
            reverse('post_new'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.filter(text='Тестовый текст').exists())


class PostEditFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create(username='TestName')
        cls.group = Group.objects.create(title='Тестовое название группы',
                                         slug='test-slug',
                                         description='Тестовое описание')
        cls.post = Post.objects.create(text='Тестовый текст поста',
                                       author=cls.user,
                                       group=cls.group)

        cls.authorized_user = Client()
        cls.authorized_user.force_login(cls.user)

        cls.form_data = {
            'text': 'Отредактированный тестовый текст поста',
            'group': cls.group.pk,
        }

    def test_forms_post_edit(self):
        """Тестирование формы редактирования постов."""

        response = self.authorized_user.post(
            reverse('post_edit',
                    kwargs={'username': 'TestName',
                            'post_id': self.post.pk}),
            data=self.form_data,
            follow=True)

        self.assertEqual(response.context['post'].text, self.form_data['text'])

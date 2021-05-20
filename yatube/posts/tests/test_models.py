from django.test import TestCase
from posts.models import Post, Group
from django.contrib.auth import get_user_model


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User = get_user_model()
        # Создаем текстовую запись в бд модели Group
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test-group',
            description='Тестовое описание'
        )

        # Создаем текстовую запись в бд модели Post
        cls.post = Post.objects.create(
            text='Заголовок текс',
            pub_date='2020-11-12',
            author=User.objects.create(username='testuser'),
            group=cls.group
        )

    def test_help_text(self):
        # Проверка help_text
        post = PostModelTest.post
        field_help_text = {
            'text': 'Заполните текстом данное поле',
            'group': 'Выберите группу'
        }

        for value, expected in field_help_text.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected)

    def test_verbose_name(self):
        # Проверка verbose_name
        post = PostModelTest.post
        field_verbose_name = {
            'text': 'Текст',
            'group': 'Группа'
        }

        for value, expected in field_verbose_name.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected)

    def test_is_str_post(self):
        # Тест на str
        post = PostModelTest.post
        expected_object_name = post.text
        self.assertEqual(expected_object_name, str(post))

    def test_is_str_group(self):
        # Тест на str
        group = PostModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))

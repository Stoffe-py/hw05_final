from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post
from django import forms


class PostPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User = get_user_model()
        cls.user = User.objects.create(username='testUser')

        cls.group = Group.objects.create(
            title='Заголовок',
            description='Текст',
            slug='test-slug',
        )

        cls.post = Post.objects.create(
            text='Test text',
            author=PostPagesTest.user,
        )

    def setUp(self):
        super().setUp()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_pages_uses_correct_template(self):
        template_pages_names = {
            'group.html': reverse('group_posts', kwargs={'slug': 'test-slug'}),
            'index.html': reverse('index'),
            'new.html': reverse('post_new'),
        }
        for template, reverse_name in template_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_new_post_page_show_correct_context_index(self):
        response = self.authorized_client.get(reverse('post_new'))
        form_fields = {
            'text': forms.CharField,
            'group': forms.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_group_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('group_posts', kwargs={'slug': 'test-slug'})
        )
        self.assertEqual(response.context.get('group').title, 'Заголовок')
        self.assertEqual(response.context.get('group').description, 'Текст')
        self.assertEqual(response.context.get('group').slug, 'test-slug')

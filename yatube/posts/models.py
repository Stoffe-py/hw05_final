from django.db import models

from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Текст',
                            help_text='Заполните текстом данное поле')
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="posts")
    group = models.ForeignKey("Group", blank=True, null=True,
                              on_delete=models.SET_NULL,
                              related_name="g_posts",
                              verbose_name='Группа',
                              help_text='Выберите группу')
    # 6 sprint images
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    class Meta():
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name='Комментарий',
                             help_text='Введите текст поста')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField(verbose_name='Комментарий',
                            help_text='Введите текст коммента')
    created = models.DateTimeField(verbose_name='Дата публикации коммента',
                                   auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=CASCADE,
                               related_name='following')

from django.contrib.auth import get_user_model
from django.db import models

from .constants import LIMIT_SYMBOLS, LIMIT_SYMBOLS_MAX

User = get_user_model()


class PublishCreatModel(models.Model):
    """
    Абстрактная модель для постов.

    Эта модель добавляет к наследникам флаг is_published и дату создания.
    Используется как база для других моделей,
    требующих отслеживание публикации и времени создания.
    """

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True
        default_related_name = 'related_objects'


class Category(PublishCreatModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        max_length=64,
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        if len(self.title) > LIMIT_SYMBOLS_MAX:
            return self.title[:LIMIT_SYMBOLS] + '...'
        return self.title


class Location(PublishCreatModel):
    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        if len(self.name) > LIMIT_SYMBOLS_MAX:
            return self.name[:LIMIT_SYMBOLS] + '...'
        return self.name


class Post(PublishCreatModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    image = models.ImageField(
        'Фото',
        upload_to='blog_images',
        blank=True,
        null=True
    )
    pub_date = models.DateTimeField(
        auto_now_add=False,
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время '
            'в будущем — можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
        related_name='posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        if len(self.title) > LIMIT_SYMBOLS_MAX:
            return self.title[:LIMIT_SYMBOLS] + '...'
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        default='',
        verbose_name='Комментарий',
        max_length=5000,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone

from blog.models import Post
from .constants import POSTS_PER_PAGE


def get_base_queryset(manager=Post.objects,
                      filter_published=False,
                      comment_count=False):
    """
    Возвращает QuerySet с опциональными фильтрациями и аннотациями.

    Args:
        manager: Менеджер модели
        first_flag: Если True, применяет дополнительную фильтрацию
        second_flag: Если True, добавляет аннотацию и сортировку
    """
    queryset = manager.select_related(
        'category',
        'author',
        'location')

    if filter_published:
        queryset = queryset.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        )

    if comment_count:
        queryset = queryset.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    return queryset


def get_paginated_page(request, queryset, page_size=POSTS_PER_PAGE):
    """
    Функция для пагинации

    Args:
        request: HttpRequest объект
        queryset: QuerySet для пагинации
        page_size: количество элементов на странице (по умолчанию из settings)

    """
    paginator = Paginator(queryset, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


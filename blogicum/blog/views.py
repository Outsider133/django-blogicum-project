from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .constants import POSTS_PER_PAGE
from .forms import CommentForm, PostForm
from .models import Category, Comment, Post
from .utils import get_base_queryset, get_paginated_page


class CheckAuthorMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            return redirect('blog:post_detail', post_id=obj.id)
        return super().dispatch(request, *args, **kwargs)


class RegistrationView(CreateView):
    """Регистрация новых пользователей c автовходом."""

    model = User
    form_class = UserCreationForm
    template_name = 'registration/registration_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)
        return response

    def get_success_url(self):
        return reverse('blog:index')


class IndexListView(ListView):
    """Главная страница с списком всех публикаций."""

    model = Post
    template_name = 'blog/index.html'
    paginate_by = POSTS_PER_PAGE

    def get_queryset(self):
        """Возвращаем базовый queryset для отображения на главной странице."""
        return get_base_queryset()


# посты


class PostDetailView(DetailView):
    """Отоброжение полной информации из публикации."""

    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        return super().get_queryset().select_related('author').annotate(
            comments_count=Count('comments')
        )

    def get_context_data(self, **kwargs):
        """Получаем базовый контекст и добавляем дополнительные данные."""
        context = super().get_context_data(**kwargs)
        post = self.object
        context['comments'] = post.comments.all()
        context['form'] = CommentForm()
        return context

    def get_object(self):
        post = super().get_object()
        if self.request.user != post.author:
            return get_object_or_404(
                get_base_queryset
                (comment_count=False),
                pk=self.kwargs['post_id']
            )
        return post


def category_posts(request, category_slug):
    """Отображение всех публикаций определённой категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = get_base_queryset(
        manager=category.posts,
    )
    page_obj = get_paginated_page(request, post_list)
    return render(
        request,
        "blog/category.html",
        {"category": category, 'page_obj': page_obj}
    )


class CreatePostView(LoginRequiredMixin, CreateView):
    """Создание публикации."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class EditPostView(LoginRequiredMixin, CheckAuthorMixin, UpdateView):
    """Редактирование публикации."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.id}
        )


@login_required
def delete_post(request, post_id):
    """Удаление публикации."""
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    form = PostForm(instance=post)
    if post.author != request.user:
        return redirect('blog:post_detail', pk=post.post_id)

    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=post.author)
    return render(request, 'blog/create.html', {'form': form, 'post': post})


# комментарии


class AddCommentView(LoginRequiredMixin, CreateView):
    """Оставляет комментарий под публикацией."""

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comments.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.author = self.request.user
        return super().form_valid(form)


class SuccessUrlMixin:
    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post.id}
        )


class EditCommentView(
    LoginRequiredMixin,
    CheckAuthorMixin,
    SuccessUrlMixin,
    UpdateView
):
    """Редактирование комментария."""

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'


class DeleteCommentView(
    LoginRequiredMixin,
    CheckAuthorMixin,
    SuccessUrlMixin,
    DeleteView
):
    """Удаление комментария."""

    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'


# Пользователи


def profile_view(request, username):
    """Профиль пользователя с подробной информацией."""
    profile = get_object_or_404(User, username=username)
    is_owner = (request.user == profile)
    publications = get_base_queryset(
        manager=profile.posts,
        filter_published=not is_owner,
    )
    page_obj = get_paginated_page(request, publications)
    context = {
        'profile': profile,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    """Редактирование информации о пользователе."""
    form = UserChangeForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/user.html', {'form': form})

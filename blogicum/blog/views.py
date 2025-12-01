from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, UpdateView, ListView
)

from .constants import POSTS_PER_PAGE
from .forms import PostForm, CommentForm
from .models import Category, Post, Comment
from .utils import get_base_queryset, get_paginated_page


class RegistrationView(CreateView):
    """Регистрация новых пользователей."""

    model = User
    form_class = UserCreationForm
    template_name = 'registration/registration_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)
        return response

    def get_success_url(self):
        return reverse_lazy('blog:index')


class IndexListView(ListView):
    """Главная страница с списком всех публикаций."""

    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = POSTS_PER_PAGE
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        """Возвращаем базовый queryset для отображения на главной странице."""
        return get_base_queryset(
            filter_published=True,
            comment_count=True)


# посты


class PostDetailView(DetailView):
    """Отоброжение полной информации из публикации."""

    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        """Получаем базовый контекст и можем добавить дополнительные данныe."""
        context = super().get_context_data(**kwargs)
        post = self.object
        context['comments'] = Comment.objects.filter(
            post=post)
        context['form'] = CommentForm()
        return context

    def get_object(self):
        post = get_object_or_404(
            get_base_queryset(),
            pk=self.kwargs['post_id']
        )

        if self.request.user != post.author:
            post = get_object_or_404(
                get_base_queryset(filter_published=True),
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
        filter_published=True,
        comment_count=True
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
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class EditPostView(LoginRequiredMixin, UpdateView):
    """Редактирование публикации."""

    model = Post
    form = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    fields = [
        'title',
        'text',
        'category',
        'location',
        'is_published',
        'pub_date'
    ]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.object.id}
        )

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, id=self.kwargs['post_id'])


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
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditCommentView(LoginRequiredMixin, UpdateView):
    """Редактирование комментария."""

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, pk=self.kwargs['comment_id'])

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return redirect('blog:post_detail', post_id=comment.post.id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.object.post.id}
        )


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    """Удаление комментария."""

    model = Comment
    template_name = 'blog/comment.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, pk=self.kwargs['comment_id'])

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return redirect('blog:post_detail', post_id=comment.post.id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.object.post.id}
        )


# Пользователи


def profile_view(request, username):
    """Профиль пользователя с подробной информацией."""
    profile = get_object_or_404(User, username=username)
    is_owner = (request.user == profile)
    publications = get_base_queryset(
        manager=profile.posts,
        filter_published=not is_owner,
        comment_count=True
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

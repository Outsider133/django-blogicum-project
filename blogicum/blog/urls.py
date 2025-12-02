from django.urls import path
from django.contrib.auth.views import PasswordChangeView

from . import views


app_name = 'blog'


urlpatterns = [
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path(
        'profile/password/',
        PasswordChangeView.as_view(
            template_name='registration/password_change_form.html',
        ),
        name='password_change'
    ),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('', views.IndexListView.as_view(), name='index'),
    path(
        'posts/<int:post_id>/edit/',
        views.EditPostView.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<int:post_id>/delete/',
        views.delete_post,
        name='delete_post'
    ),
    path(
        'posts/create/',
        views.CreatePostView.as_view(),
        name='create_post'
    ),
    path(
        'posts/<int:post_id>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'posts/<int:post_id>/comment/',
        views.AddCommentView.as_view(),
        name='add_comment'
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        views.EditCommentView.as_view(),
        name='edit_comment'
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        views.DeleteCommentView.as_view(),
        name='delete_comment'
    ),
    path(
        'category/<slug:category_slug>/',
        views.category_posts,
        name='category_posts'
    ),
]

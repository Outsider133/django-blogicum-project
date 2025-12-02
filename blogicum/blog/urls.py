from django.contrib.auth.views import PasswordChangeView
from django.urls import include, path

from . import views


app_name = 'blog'


profile_urls = [
    path('edit/', views.edit_profile, name='edit_profile'),
    path(
        'password/',
        PasswordChangeView.as_view(
            template_name='registration/password_change_form.html',
        ),
        name='password_change'
    ),
    path('<str:username>/', views.profile_view, name='profile'),
]


posts_urls = [
    path(
        '<int:post_id>/edit/',
        views.EditPostView.as_view(),
        name='edit_post'
    ),
    path(
        '<int:post_id>/delete/',
        views.delete_post,
        name='delete_post'
    ),
    path(
        'create/',
        views.CreatePostView.as_view(),
        name='create_post'
    ),
    path(
        '<int:post_id>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
]


urlpatterns = [
    path('profile/', include(profile_urls)),
    path('', views.IndexListView.as_view(), name='index'),
    path('posts/', include(posts_urls)),
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

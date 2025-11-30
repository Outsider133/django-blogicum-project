from django.urls import include, path

from . import views


app_name = 'blog'


profile_urls = [
    path('edit/', views.edit_profile, name='edit_profile'),
    path('<str:username>/', views.profile_view, name='profile'),
]


urlpatterns = [
    path('profile/', include(profile_urls)),
    path('', views.IndexListView.as_view(), name='index'),
    path(
        'posts/<int:post_id>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'posts/create/',
        views.CreatePostView.as_view(),
        name='create_post'
    ),
    path(
        'posts/<int:pk>/edit/',
        views.EditPostView.as_view(),
        name='edit_post'
    ),
    path(
        'category/<slug:category_slug>/',
        views.category_posts,
        name='category_posts'
    ),
    path(
        'posts/<int:post_id>/delete/',
        views.delete_post,
        name='delete_post'
    ),
    path(
        'posts/<int:post_id>/comment/',
        views.AddCommentView.as_view(),
        name='add_comment'
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:pk>/',
        views.EditCommentView.as_view(),
        name='edit_comment'
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:pk>/',
        views.DeleteCommentView.as_view(),
        name='delete_comment'
    ),
]

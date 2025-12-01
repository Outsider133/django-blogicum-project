from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import PasswordChangeView
from django.conf.urls.static import static
from django.urls import include, path

from blog import views


handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/profile/', views.IndexListView.as_view(), name='index'),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('blog.urls', namespace='blog')),
    path(
        'auth/registration/',
        views.RegistrationView.as_view(),
        name='registration'
    ),
    path(
        'auth/password_change/',
        PasswordChangeView.as_view(
            template_name='registration/password_change_form.html',
        ),
        name='password_change'
    ),
    path('pages/', include('pages.urls')),
    path('', include('blog.urls')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

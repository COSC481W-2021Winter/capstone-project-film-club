"""filmclub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),  # Home/landing screen
    path('accounts/', include('django.contrib.auth.urls')),  # Enable Django auth app
    path('register/', views.register, name='register'),  # New user signup screen
    path('genres/', views.genres, name = 'genres'),  # Genre selection screen
    path('m/add', views.add_movie, name = 'add_movie'),  # Movie profile screen
    path('m/<int:id>', views.movie, name = 'movie'),  # Movie profile screen

    path("password-change/", auth_views.PasswordChangeView.as_view( # Password reset screen
        template_name='registration/password-reset/change_password.html',
        success_url = '/'),
        name = "password_change"
    ),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password-reset/password_reset.html',
        subject_template_name='registration/password-reset/password_reset_subject.txt',
        email_template_name='registration/password-reset/password_reset_email.html',
        success_url='/accounts/login/'), name='password_reset'
    ),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view( template_name='registration/password-reset/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password-reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password-reset/password_reset_complete.html'), name='password_reset_complete'),
    path("welcome/", views.welcome, name = "send welcome email"),

    path('watch/', views.watch, name = 'watch'),
    path('friend/', views.friend, name = 'friend'),

    path('<str:username>/', views.profile, name='profile'),  # Profile screen
]

#### URL'S INCLUDED BY USING DJANGO AUTH ####################
# accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']
################################################################

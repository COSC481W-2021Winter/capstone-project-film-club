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
    path('about/', views.about, name='about'), # about us page
    path('register/', views.register, name='register'),  # New user signup screen
    path('genres/', views.genres, name = 'genres'),  # Genre selection screen
    path('search', views.search, name = 'search'),  # Search screen
    path('m/<int:id>/', views.movie, name = 'movie'),  # Movie profile screen
    path("welcome/", views.welcome, name = "send welcome email"),
    path('reviews/<int:page>/', views.get_home_reviews, name = 'home_reviews'),
    path('u/<str:username>/', views.profile, name='profile'),  # Profile screen
    path('r/<int:review_id>/', views.review, name='review'),  # Review screen
    path('r/<int:review_id>/like', views.review_like, name='review_like'),  # Review like action
    path('r/<int:review_id>/comment', views.review_comment, name='review_comment'),  # Review comment action
    path('accounts/', include('django.contrib.auth.urls')),  # Enable Django auth app

    path('bug_reporting_page/', views.bug_reporting_page, name='bug_reporting_page'), # Bug reporting page
    path('watch/', views.watch, name = 'watch'),
    path('friend/', views.friend, name = 'friend'),
    path('u/<str:username>/edit/', views.edit_profile, name='edit_profile'),
]
handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'
handler403 = 'core.views.error_403'
handler400 = 'core.views.error_400'

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

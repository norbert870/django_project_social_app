from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('user/<int:user_id>/follow/', views.follow_user, name='follow_user'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
    path('users/', views.user_list, name='user_list'),
]
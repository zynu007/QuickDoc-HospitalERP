from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_home, name='blog_home'),
    path('post/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('create/', views.blog_create, name='blog_create'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('publish/<int:post_id>/', views.publish_post, name='publish_post'),
]
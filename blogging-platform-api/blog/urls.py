from django.urls import path
from .views import create_post, post_list, update_post, delete_post, posts_by_category, posts_by_author
from .views import (
    create_post,
    post_list,
    update_post,
    delete_post,
    posts_by_category,
    posts_by_author,
    search_posts,
)

urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/new/', create_post, name='create_post'),
    path('post/edit/<int:post_id>/', update_post, name='update_post'),
    path('post/delete/<int:post_id>/', delete_post, name='delete_post'),
    path('category/<str:category>/', posts_by_category, name='posts_by_category'),
    path('author/<str:author_username>/', posts_by_author, name='posts_by_author'),
    path('search/', search_posts, name='search_posts'),
]


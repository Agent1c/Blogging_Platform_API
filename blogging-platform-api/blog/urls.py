from django.urls import path
from .views import (
    create_post,
    post_list,
    update_post,
    delete_post,
    posts_by_category,
    posts_by_author,
    search_posts,
)

app_name = 'blog'

urlpatterns = [
    path('', post_list, name='post_list'),
    path('author/<str:author_username>/', posts_by_author, name='posts_by_author'),
    path('category/<str:category_name>/', posts_by_category, name='posts_by_category'),
    path('post/<int:pk>/edit/', update_post, name='update_post'),
    path('post/<int:pk>/delete/', delete_post, name='delete_post'),
    path('search/', search_posts, name='search_posts'),
    path('post/new/', create_post, name='create_post'),
]


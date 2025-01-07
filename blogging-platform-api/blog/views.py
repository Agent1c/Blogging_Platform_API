from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import BlogPost
from .forms import BlogPostForm
from django.db.models import Q
from datetime import datetime


# Post list
def post_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the author to the logged-in user
            post.save()
            return redirect('post_list')
    else:
        form = BlogPostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def update_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if post.author != request.user.username:  # Check if the user is the author
        return redirect('post_list')

    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if post.author != request.user.username:  # Check if the user is the author
        return redirect('post_list')

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


def posts_by_category(request, category):
    posts = BlogPost.objects.filter(category=category)
    
    # Optional filtering by published date
    published_after = request.GET.get('published_after')
    if published_after:
        published_after_date = datetime.strptime(published_after, '%Y-%m-%d')
        posts = posts.filter(published_date__gte=published_after_date)

    # Optional filtering by tags
    tags = request.GET.get('tags')
    if tags:
        tags_list = [tag.strip() for tag in tags.split(',')]
        posts = posts.filter(tags__in=tags_list)

    return render(request, 'blog/posts_by_category.html', {'posts': posts, 'category': category})

def posts_by_author(request, author_username):
    author = get_object_or_404(User, username=author_username)
    posts = BlogPost.objects.filter(author=author)

    # Optional filtering by published date
    published_after = request.GET.get('published_after')
    if published_after:
        published_after_date = datetime.strptime(published_after, '%Y-%m-%d')
        posts = posts.filter(published_date__gte=published_after_date)

    # Optional filtering by tags
    tags = request.GET.get('tags')
    if tags:
        tags_list = [tag.strip() for tag in tags.split(',')]
        posts = posts.filter(tags__in=tags_list)

    return render(request, 'blog/posts_by_author.html', {'posts': posts, 'author': author})

def search_posts(request):
    query = request.GET.get('q')  # Search query
    category = request.GET.get('category')  # Filter by category
    published_after = request.GET.get('published_after')  # Filter by published date
    tags = request.GET.get('tags')  # Filter by tags

    # Start with all blog posts
    posts = BlogPost.objects.all()

    # Filter by search query if provided
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(tags__icontains=query)
        )

    # Filter by category if provided
    if category:
        posts = posts.filter(category=category)

    # Filter by published date if provided
    if published_after:
        published_after_date = datetime.strptime(published_after, '%Y-%m-%d')
        posts = posts.filter(published_date__gte=published_after_date)

    # Filter by tags if provided
    if tags:
        tags_list = [tag.strip() for tag in tags.split(',')]
        posts = posts.filter(tags__in=tags_list)

    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')
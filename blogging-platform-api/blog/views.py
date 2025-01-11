from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import BlogPost
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import BlogPostForm, UserRegistrationForm
from django.db.models import Q
from datetime import datetime
from .forms import UserProfileForm



@login_required(login_url='/users/login/')
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save the many-to-many data for the form
            return redirect('post_list')
    else:
        form = BlogPostForm(user=request.user)
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def update_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.author != request.user:
        return redirect('post_list')
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = BlogPostForm(instance=post, user=request.user)
    return render(request, 'blog/update_post.html', {'form': form})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.author != request.user:
        return redirect('post_list')
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/delete_post.html', {'post': post})

def category_view(request, category_name):
       posts = BlogPost.objects.filter(category__name=category_name)
       return render(request, 'blog/category.html', {'posts': posts})

# Post list
def post_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def posts_by_category(request, category):
    posts = BlogPost.objects.filter(category=category)
    published_after = request.GET.get('published_after')
    if published_after:
        published_after_date = datetime.strptime(published_after, '%Y-%m-%d')
        posts = posts.filter(published_date__gte=published_after_date)
    tags = request.GET.get('tags')
    if tags:
        tags_list = [tag.strip() for tag in tags.split(',')]
        posts = posts.filter(tags__in=tags_list)
    return render(request, 'blog/posts_by_category.html', {'posts': posts, 'category': category})

def posts_by_author(request, author_username):
    author = get_object_or_404(User, username=author_username)
    posts = BlogPost.objects.filter(author=author)
    published_after = request.GET.get('published_after')
    if published_after:
        published_after_date = datetime.strptime(published_after, '%Y-%m-%d')
        posts = posts.filter(published_date__gte=published_after_date)
    tags = request.GET.get('tags')
    if tags:
        tags_list = [tag.strip() for tag in tags.split(',')]
        posts = posts.filter(tags__in=tags_list)
    return render(request, 'blog/posts_by_author.html', {'posts': posts, 'author': author})


def search_posts(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    published_after = request.GET.get('published_after')
    tags = request.GET.get('tags')
    posts = BlogPost.objects.all()
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(tags__icontains=query)
        )
    if category:
        posts = posts.filter(category=category)
    if published_after:
        published_after_date = datetime.strptime(published_after, '%Y-%m-%d')
        posts = posts.filter(published_date__gte=published_after_date)
    if tags:
        tags_list = [tag.strip() for tag in tags.split(',')]
        posts = posts.filter(tags__in=tags_list)
    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# def user_login(request):
#     return render(request, 'registration/login.html')

def login(request):
    return render(request, 'users/login.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home') 
    

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('post_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'registration/profile.html', {'form': form})
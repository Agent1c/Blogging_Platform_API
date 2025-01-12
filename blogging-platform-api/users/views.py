from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

def rate_limit(key_prefix, limit=5, period=60):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            key = f"{key_prefix}_{request.META.get('REMOTE_ADDR')}"
            attempts = cache.get(key, 0)
            if attempts >= limit:
                logger.warning(f"Rate limit exceeded for IP: {request.META.get('REMOTE_ADDR')}")
                raise PermissionDenied("Too many attempts. Please try again later.")
            cache.set(key, attempts + 1, period)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                # Validate password strength
                validate_password(form.cleaned_data['password1'])
                user = form.save()
                logger.info(f"New user registered: {user.username}")
                login(request, user)
                messages.success(request, 'Registration successful!')
                return redirect('profile')
            except ValidationError as e:
                form.add_error('password1', e)
                logger.warning(f"Password validation failed for new registration attempt")
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@rate_limit('login', limit=5, period=300)
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Set session expiry and last login
            request.session.set_expiry(3600)  # 1 hour
            request.session['last_login'] = str(timezone.now())
            
            logger.info(f"Successful login for user: {user.username}")
            
            next_url = request.GET.get('next')
            if next_url and is_safe_url(next_url, allowed_hosts=None):
                return redirect(next_url)
            return redirect('profile')
        else:
            logger.warning(f"Failed login attempt for username: {request.POST.get('username')}")
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})

@login_required
@cache_page(60 * 15)  # Cache for 15 minutes
def profile_view(request):
    try:
        user_data = {
            'user': request.user,
            'profile': getattr(request.user, 'profile', None),
            'last_login': request.session.get('last_login', 'First visit')
        }
        return render(request, 'users/profile.html', user_data)
    except Exception as e:
        logger.error(f"Error in profile view for user {request.user.username}: {str(e)}")
        messages.error(request, 'An error occurred while loading your profile.')
        return redirect('home')

@require_http_methods(["POST"])
def logout_view(request):
    try:
        username = request.user.username
        logout(request)
        logger.info(f"User logged out: {username}")
        messages.success(request, 'You have been successfully logged out.')
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
    return redirect('login')
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Include users.urls with 'users/' prefix
    path('blog/', include('blog.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', RedirectView.as_view(url='blog/', permanent=True)),  # Redirect root URL to 'blog/'
]
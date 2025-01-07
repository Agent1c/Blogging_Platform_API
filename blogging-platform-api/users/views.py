from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from .serializers import UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
           user = form.save()
           login(request, user)
           return redirect('post_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})
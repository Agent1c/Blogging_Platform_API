from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'author', 'category', 'tags']
        widgets = {
            'tags': forms.TextInput(attrs={'placeholder': 'Comma-separated tags (optional)'}),
        }


from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import BlogPost  # Ensure BlogPost model is imported

class BlogPostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = BlogPost.objects.all()
        # Serialize and return the posts
        return Response({'posts': [post.title for post in posts]})  # Example serialization
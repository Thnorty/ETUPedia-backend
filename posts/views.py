from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from posts.models import Post


# Create your views here.
class GetPostsApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        posts = Post.objects.all().order_by('-timestamp')
        response = []
        for post in posts:
            response.append({
                'author': post.author.name,
                'content': post.content,
                'timestamp': post.timestamp
            })
        return JsonResponse(response, status=200)
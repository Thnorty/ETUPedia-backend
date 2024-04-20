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
        posts = Post.objects.all().order_by('-created_at')
        response = []
        for post in posts:
            response.append({
                'id': post.id,
                'author_name': post.author.student.name + ' ' + post.author.student.surname,
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at.strftime('%H:%M %d %B %Y')
            })
        return JsonResponse(response, safe=False)

from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import pytz

from posts.models import Post, Topic, PostComment


# Create your views here.
class GetPostsApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        posts = Post.objects.all().order_by('-created_at')
        response = []
        for post in posts:
            created_at = post.created_at.astimezone(pytz.timezone('Europe/Istanbul')).strftime('%H:%M %d %B %Y')
            response.append({
                'id': post.id,
                'is_owner': post.author == request.user.profile,
                'topic': {
                    'name': post.topic.name,
                    'order': post.topic.order
                },
                'author_name': post.author.student.name + ' ' + post.author.student.surname,
                'title': post.title,
                'content': f'{post.content[:100]}...' if len(post.content) > 100 else post.content,
                'created_at': created_at,
                'likes': post.likes.count(),
                'liked': post.likes.filter(id=request.user.profile.id).exists()
            })
        return JsonResponse(response, safe=False)


class CreatePostApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        author = request.user.profile
        topic_order = request.data.get('topic_order')
        title = request.data.get('title')
        content = request.data.get('content')
        topic = Topic.objects.get(order=topic_order)
        post = Post.objects.create(author=author, topic=topic, title=title, content=content)
        post.save()
        return JsonResponse({'message': 'Post created successfully'}, status=201)


class EditPostApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        post_id = request.data.get('post_id')
        post = Post.objects.get(id=post_id)
        if post.author != request.user.profile:
            return JsonResponse({'message': 'You are not the owner of this post'}, status=403)
        topic_order = request.data.get('topic_order')
        post.topic = Topic.objects.get(order=topic_order)
        post.title = request.data.get('title')
        post.content = request.data.get('content')
        post.save()
        return JsonResponse({'message': 'Post edited successfully'}, status=200)


class DeletePostApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        post_id = request.data.get('post_id')
        post = Post.objects.get(id=post_id)
        if post.author != request.user.profile:
            return JsonResponse({'message': 'You are not the owner of this post'}, status=403)
        post.delete()
        return JsonResponse({'message': 'Post deleted successfully'}, status=200)


class CreateCommentApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        author = request.user.profile
        post_id = request.data.get('forum_id')
        content = request.data.get('content')
        post = Post.objects.get(id=post_id)
        comment = PostComment.objects.create(author=author, post=post, content=content)
        comment.save()
        return JsonResponse({'message': 'Comment created successfully'}, status=201)


class EditCommentApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        comment_id = request.data.get('comment_id')
        comment = PostComment.objects.get(id=comment_id)
        if comment.author != request.user.profile:
            return JsonResponse({'message': 'You are not the owner of this comment'}, status=403)
        comment.content = request.data.get('content')
        comment.save()
        return JsonResponse({'message': 'Comment edited successfully'}, status=200)


class DeleteCommentApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        comment_id = request.data.get('comment_id')
        comment = PostComment.objects.get(id=comment_id)
        if comment.author != request.user.profile:
            return JsonResponse({'message': 'You are not the owner of this comment'}, status=403)
        comment.delete()
        return JsonResponse({'message': 'Comment deleted successfully'}, status=200)


class GetPostInfoApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        post_id = request.data.get('forum_id')
        post = Post.objects.get(id=post_id)
        created_at = post.created_at.astimezone(pytz.timezone('Europe/Istanbul')).strftime('%H:%M %d %B %Y')
        response_post = {
            'id': post.id,
            'is_owner': post.author == request.user.profile,
            'topic': {
                'name': post.topic.name,
                'order': post.topic.order
            },
            'author_name': post.author.student.name + ' ' + post.author.student.surname,
            'title': post.title,
            'content': post.content,
            'created_at': created_at,
            'likes': post.likes.count(),
            'liked': post.likes.filter(id=request.user.profile.id).exists()
        }
        comments = post.postcomment_set.all().order_by('-created_at')
        response_comments = []
        for comment in comments:
            created_at = comment.created_at.astimezone(pytz.timezone('Europe/Istanbul')).strftime('%H:%M %d %B %Y')
            response_comments.append({
                'id': comment.id,
                'is_owner': comment.author == request.user.profile,
                'author_name': comment.author.student.name + ' ' + comment.author.student.surname,
                'content': comment.content,
                'created_at': created_at,
                'likes': comment.likes.count(),
                'liked': comment.likes.filter(id=request.user.profile.id).exists()
            })
        response = {
            'post': response_post,
            'comments': response_comments
        }
        return JsonResponse(response, safe=False)


class LikePostApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        post_id = request.data.get('forum_id')
        post = Post.objects.get(id=post_id)
        profile = request.user.profile
        if post.likes.filter(id=profile.id).exists():
            post.likes.remove(profile)
            return JsonResponse({'message': 'Post unliked successfully'}, status=200)
        post.likes.add(profile)
        return JsonResponse({'message': 'Post liked successfully'}, status=200)


class LikeCommentApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        comment_id = request.data.get('comment_id')
        comment = PostComment.objects.get(id=comment_id)
        profile = request.user.profile
        if comment.likes.filter(id=profile.id).exists():
            comment.likes.remove(profile)
            return JsonResponse({'message': 'Comment unliked successfully'}, status=200)
        comment.likes.add(profile)
        return JsonResponse({'message': 'Comment liked successfully'}, status=200)


class GetTopicsApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        topics = Topic.objects.all().order_by('order')
        response = []
        for topic in topics:
            response.append({
                'order': topic.order,
                'name': topic.name
            })
        return JsonResponse(response, safe=False)

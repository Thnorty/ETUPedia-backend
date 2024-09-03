from django.db import models

from api.models import Profile


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Profile, related_name='likes', blank=True)

    class Meta:
        ordering = ['-created_at']

    def like_count(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.author.student.name + ' ' + self.author.student.surname} - {self.title}'


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Profile, related_name='comment_likes', blank=True)

    class Meta:
        ordering = ['created_at']

    def like_count(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.author.student.name + self.author.student.surname} - {self.content[:20]}'


class Topic(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

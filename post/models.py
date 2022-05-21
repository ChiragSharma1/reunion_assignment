from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=1000, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return self.user.username + ' ' + self.post.title


class Comment(models.Model):
    comment_text = models.TextField(max_length=1000)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_text + ' by ' + self.user.username + ' on ' + self.post.title + ' '

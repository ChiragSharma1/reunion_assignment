from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number_of_followers = models.IntegerField(default=0)
    number_of_followings = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class UserFollower(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')

    class Meta:
        unique_together = ('user', 'follower')

    def __str__(self):
        return self.user.username + " 's follower - " + self.follower.username

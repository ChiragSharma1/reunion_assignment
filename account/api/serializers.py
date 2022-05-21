from rest_framework import serializers
from django.contrib.auth import get_user_model
from account.models import UserFollower, UserProfile


UserModel = get_user_model()


class UserProfileSerialiser(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        extra_fields = ['user_name']
        model = UserProfile
        read_only_fields = ('user',)
        fields = ('user_name', 'number_of_followers', 'number_of_followings',)

    def get_user_name(self, object):
        return object.user.first_name + " " + object.user.last_name


class UserFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollower
        fields = ('user', 'follower')

    # numer of people following this user
    def get_total_follower(self, obj):
        return UserFollower.objects.filter(user=obj.id).count()

    # number of people this user is following
    def get_total_following(self, obj):
        return UserFollower.objects.filter(follower=obj.id).count()

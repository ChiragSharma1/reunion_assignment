from rest_framework import serializers
from django.contrib.auth import get_user_model
from post.models import Post, Like, Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        read_only_fields = ('user', 'post',)
        fields = ('id', 'post', 'user', 'comment_text',)


class PostSerializer(serializers.ModelSerializer):

    comments = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='comment_text'
    )
    number_of_likes = serializers.SerializerMethodField()
    number_of_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        read_only_fields = ('user',)
        fields = ('id', 'title', 'description', 'comments', 'number_of_comments',
                  'number_of_likes', 'created_time',)

    def get_number_of_likes(self, object):
        # this will return number of likes on this post
        return Like.objects.filter(post=object.id).count()

    def get_number_of_comments(self, object):
        return Comment.objects.filter(post=object.id).count()


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('user', 'post',)

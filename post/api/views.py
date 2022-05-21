from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from post.models import Post, Comment, Like
from post.api.serializers import PostSerializer, LikeSerializer, CommentSerializer


class PostAV(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            context = {
                "post_id": serializer['id'].value,
                "title": serializer['title'].value,
                "description": serializer['description'].value,
                "created_time": serializer['created_time'].value,
            }
            return Response(data=context, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailsAV(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            post_query = Post.objects.get(id=pk)
        except:
            return Response({"message": "Post with such id dosent exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PostSerializer(post_query)

        # making context as data that we need to send
        context = {
            "postId": serializer['id'].value,
            "number of likes": serializer['number_of_likes'].value,
            "number of comments": serializer['number_of_comments'].value,
        }
        # print("-----------------", context)
        return Response(data=context, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            post_query = Post.objects.get(id=pk)
        except:
            return Response({"message": "Post with such id dosent exists"}, status=status.HTTP_400_BAD_REQUEST)

        if post_query.user != request.user:
            return Response({'message': 'Current user is not owner of this post , so cannot delete it'}, status=status.HTTP_400_BAD_REQUEST)

        # deleting post
        post_query.delete()
        return Response({'message': 'Post Deleted Successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_view(request, pk):
    # like the post with id = pk by authenticated user

    try:
        post = Post.objects.get(id=pk)
    except:
        return Response({"message": "Post with such id dosent exists"}, status=status.HTTP_400_BAD_REQUEST)

    obj, create = Like.objects.get_or_create(post=post, user=request.user)
    return Response({'message': 'Post Liked Successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_view(request, pk):
    # unlike the post with id = pk by authenticated user

    try:
        post = Post.objects.get(id=pk)
    except:
        return Response({"message": "Post with such id dosent exists"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        liked_post = Like.objects.get(post=post, user=request.user)
    except:
        return Response({"message": "Post is already unliked"}, status=status.HTTP_400_BAD_REQUEST)

    liked_post.delete()
    return Response({'message': 'Unliked Post Successfully'}, status=status.HTTP_200_OK)


class CommentAV(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except:
            return Response({"message": "Post with such id dosent exists"}, status=status.HTTP_400_BAD_REQUEST)

        comment_serializer = CommentSerializer(data=request.data)
        if comment_serializer.is_valid():
            comment_serializer.save(user=request.user, post=post)
            return Response({'Comment id': comment_serializer['id'].value}, status=status.HTTP_201_CREATED)
        else:
            return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_posts_view(request):
    posts_query = Post.objects.filter(user=request.user)
    serializer = PostSerializer(posts_query, many=True)
    # print("---------", serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)

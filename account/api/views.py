from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from account.models import UserFollower, UserProfile
from account.api.serializers import UserFollowerSerializer, UserProfileSerialiser


# class ProfileAV(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         user = self.request.user
#         profile = UserProfile.objects.get(user=user)
#         profile_serializer = UserProfileSerialiser(profile)
#         return Response(profile_serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    profile_serializer = UserProfileSerialiser(profile)
    return Response(profile_serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_view(request, pk):
    #   authenticated user will follow user with id = pk

    user = request.user
    user_to_follow = get_object_or_404(User, id=pk)  # getting user to follow

    if(user == user_to_follow):
        return Response({'message': 'User can not follow itself'}, status=status.HTTP_400_BAD_REQUEST)

    if UserFollower.objects.filter(user=user_to_follow, follower=user).count() > 0:
        return Response({"message": "User already follow user(with id = pk)"}, status=status.HTTP_400_BAD_REQUEST)

    # getting their respective profiles
    user_profile = UserProfile.objects.get(
        user=user)    # getting user's profile
    user_to_follow_profile = UserProfile.objects.get(
        user=user_to_follow)   # getiing user_to_follow's profile

    # now updating  number of followers and following in respective users
    user_profile.number_of_followings = 1 + user_profile.number_of_followings
    user_to_follow_profile.number_of_followers = 1 + \
        user_to_follow_profile.number_of_followers

    # making uses follow to user with id =  pk by adding it to table UserFollower
    follow_user_queryset = UserFollower(user=user_to_follow, follower=user)

    # saving all
    follow_user_queryset.save()
    user_profile.save()
    user_to_follow_profile.save()

    return Response({'message:User follow successfully done'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_view(request, pk):
    #   authenticated user will unfollow user with id = pk

    user = request.user
    user_to_unfollow = get_object_or_404(
        User, id=pk)  # getting user to unfollow

    if (user == user_to_unfollow):
        return Response({'message:User cannot unfollow itself'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        follow_user_queryset = UserFollower.objects.get(
            user=user_to_unfollow, follower=user)
    except:
        return Response({'message: User already is not following.'}, status=status.HTTP_400_BAD_REQUEST)

    # Deleting uses_follow column from table UserFollow Table to make user unfollow user with id =  pk
    follow_user_queryset.delete()

    # getting their respective profiles
    user_profile = UserProfile.objects.get(
        user=user)    # getting user's profile
    user_to_unfollow_profile = UserProfile.objects.get(
        user=user_to_unfollow)   # getiing user_to_follow's profile

    # now updating  number of followers and following in respective users
    user_profile.number_of_followings = user_profile.number_of_followings - 1
    user_to_unfollow_profile.number_of_followers = user_to_unfollow_profile.number_of_followers - 1

    # saving all
    user_profile.save()
    user_to_unfollow_profile.save()

    return Response({'message:User unfollowing successfully done'}, status=status.HTTP_200_OK)

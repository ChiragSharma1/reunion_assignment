from django.urls import path

from post.api.views import PostAV, PostDetailsAV, like_view, unlike_view, CommentAV, all_posts_view


urlpatterns = [
    path('api/posts/<int:pk>', PostDetailsAV.as_view(), name="post_details"),
    path('api/posts/', PostAV.as_view(), name="post"),
    path('api/comment/<int:pk>', CommentAV.as_view(), name="comment"),

    path('api/like/<int:pk>', like_view, name="like"),
    path('api/unlike/<int:pk>', unlike_view, name="unlike"),
    path('api/all_posts', all_posts_view, name="all_post"),
]

from django.urls import path
from account.api.views import profile_view, follow_view, unfollow_view

urlpatterns = [
    path('api/follow/<int:pk>', follow_view, name="follow"),
    path('api/unfollow/<int:pk>', unfollow_view, name="unfollow"),
    path('api/user', profile_view, name="profile"),
]

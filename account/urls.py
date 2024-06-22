# accounts/urls.py
from django.urls import path
from .views import CreateUserView, LoginView, UserDetailAPIView, MyProfileAPIView, PostListCreateAPIView, PostDetailAPIView, LikeCreateAPIView,LikeDestroyAPIView


urlpatterns = [
    path('accounts/', CreateUserView.as_view(), name='create-account'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/<int:pk>', UserDetailAPIView.as_view(), name='user-detail'),
    path('me/', MyProfileAPIView.as_view(), name='MyProfileView'),

    path('blog/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('blog/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('like/<int:post_id>/', LikeCreateAPIView.as_view(), name='like-create'),
    path('like/<int:post_id>', LikeDestroyAPIView.as_view(), name='like-delete'),
]

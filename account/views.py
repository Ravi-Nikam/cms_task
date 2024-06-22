# accounts/views.py
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import Post, Like
from .serializers import UserSerializer, LoginSerializer, UpdateSerializer, PostSerializer, LikeSerializer
from .permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnlyPostDetail

User = get_user_model()

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    
class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    

class MyProfileAPIView(generics.RetrieveAPIView):
    """ API endpoint for getting logged-in user info - requires JWT authentication. """
    permission_classes = [permissions.IsAuthenticated, ]

    # override method
    def retrieve(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response({
            'message': 'Successfully fetched logged-in User Info.',
            'success': True,
            'status_code': status.HTTP_200_OK,
            'User_Info': {
                'email': serializer.data['email'],
                'name': serializer.data['name'],
                'created_at': request.user.created_at,
                'updated_at': request.user.updated_at
            }
        })



class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(owner=self.request.user) | Post.objects.filter(is_public=True)
        else:
            return Post.objects.filter(is_public=True)

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnlyPostDetail]

class LikeCreateAPIView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = generics.get_object_or_404(Post, pk=post_id)
        serializer.save(user=self.request.user, post=post)

class LikeDestroyAPIView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        post = generics.get_object_or_404(Post, pk=post_id)
        like = generics.get_object_or_404(Like, post=post, user=request.user)
        self.perform_destroy(like)
        return Response(status=status.HTTP_204_NO_CONTENT)
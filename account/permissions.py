from rest_framework import permissions
from .models import Post

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsOwnerOrReadOnlyPostDetail(IsOwnerOrReadOnly):
    def has_permission(self, request, view):
        post_id = view.kwargs['pk']
        post = Post.objects.get(pk=post_id)
        if post.is_public or (request.user.is_authenticated and post.owner == request.user):
            return True
        return False

from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.serializers import TodoSerializer, UserSerializer
from lists.models import Todo


class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `creator` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we will always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # If the object doesn't have a creator (i.e. anon) allow all methods.
        if not obj.creator:
            return True

        # Instance must have an attribute named `creator`.
        return obj.creator == request.user


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class TodoViewSet(viewsets.ModelViewSet):

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = (IsCreatorOrReadOnly, IsAuthenticated)

    # CREATE
    def perform_create(self, serializer):
        user = self.request.user
        creator = user if user.is_authenticated else None
        serializer.save(creator=creator)

    # READ
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        creator = user if user.is_authenticated else None
        queryset = queryset.filter(creator_id=creator)
        return queryset
    
    # PUT
    def update(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'Instance updated successfully'})
    
    # DELETE
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({'message': 'Instance deleted successfully'})


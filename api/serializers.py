from django.contrib.auth.models import User
from rest_framework import serializers

from lists.models import Todo


class UserSerializer(serializers.ModelSerializer):

    todolist = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Todo.objects.all()
    )

    class Meta:
        model = User
        fields = ("id", "username", "last_login", "date_joined", "todolists")


class TodoSerializer(serializers.ModelSerializer):

    creator = serializers.ReadOnlyField(source="creator.username")

    class Meta:
        model = Todo
        fields = (
            "id",
            "description",
            "created_at",
            "is_finished",
            "creator",
        )

from rest_framework import serializers
from .models import Post, Comment


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class UpvotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("amount_of_upvotes",)
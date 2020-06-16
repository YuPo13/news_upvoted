from rest_framework import serializers
from .models import Post, Comment
from datetime import datetime


class PostsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def post_create(self):
        author = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            author = request.user
        title = self.validated_data['title']
        link = self.validated_data['link']
        creation_date = datetime.now()

        return Post.objects.create(title=title, link=link, author=author, creation_date=creation_date)


class PostsUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"

    def post_update(self):
        author = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            author = request.user
        title = self.validated_data['title']
        link = self.validated_data['link']
        creation_date = datetime.now()

        return Post.objects.update(title=title, link=link, creation_date=creation_date)


class CommentsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    def comment_create(self):
        author = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            author = request.user

        content = self.validated_data['content']

        request_stream = str(request.stream).strip("'>")
        slash_index = request_stream.index("/")
        post = request_stream[(slash_index + 1):]
        news = Post.objects.filter(id=post).first()

        creation_date = datetime.now()

        return Comment.objects.create(author=author, content=content, news=news, creation_date=creation_date)


class CommentsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    def comment_update(self):
        author = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            author = request.user

        content = self.validated_data['content']

        request_stream = str(request.stream).strip("'>")
        news_start_index = request_stream.index("/") + 1
        news_end_index = request_stream.rindex("/")
        post = request_stream[news_start_index:news_end_index]
        news = Post.objects.filter(id=post).first()

        creation_date = datetime.now()

        return Comment.objects.create(author=author, content=content, news=news, creation_date=creation_date)


class UpvotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("amount_of_upvotes",)
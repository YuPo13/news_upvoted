from rest_framework import generics, response, status, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .models import Post, Comment
from .serializers import PostsCreateSerializer, PostsUpdateSerializer, CommentsCreateSerializer, \
    CommentsUpdateSerializer, UpvotesSerializer


def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes
            # this call is needed for request permissions
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)
        return decorated_func
    return decorator


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of profile to view or edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IndexView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PostsCreateSerializer
    queryset = Post.objects.all().order_by("-amount_of_upvotes", "-creation_date")


class AllCommentsView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CommentsCreateSerializer
    queryset = Comment.objects.all().order_by("-creation_date")


class NewsSubmitView(generics.CreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = PostsCreateSerializer


class NewsCommentsView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CommentsCreateSerializer
    lookup_url_kwarg = 'news_pk'

    def get_queryset(self):
        post_id = self.kwargs['news_pk']
        return Comment.objects.filter(news=post_id).order_by("-creation_date")

    @method_permission_classes((IsAuthenticatedOrReadOnly,))
    def post(self, request, *args, **kwargs):
        new_comment = self.create(request, *args, **kwargs)

        return response.Response({"success": "Your comment has been added"})


class NewsEditView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwner,)
    serializer_class = PostsUpdateSerializer
    lookup_url_kwarg = 'news_pk'

    def get_queryset(self):
        post_id = self.kwargs['news_pk']
        return Post.objects.filter(pk=post_id)


class CommentEditView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwner,)
    serializer_class = CommentsUpdateSerializer
    lookup_url_kwarg = 'comment_pk'

    def get_queryset(self):
        comment_id = self.kwargs['comment_pk']
        return Comment.objects.filter(pk=comment_id)


class NewsUpvoteView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = UpvotesSerializer
    lookup_url_kwarg = 'news_pk'

    def get_queryset(self):
        post_id = self.kwargs['news_pk']
        return Post.objects.filter(id=post_id)

    def put(self, request, *args, **kwargs):
        post = self.get_queryset().first()

        if not post:
            return response.Response({"error": "Such post does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if post.author == request.user:
            return response.Response({"error": "You can't upvote your own posts"})

        post.amount_of_upvotes += 1
        post.save(force_update=True)
        return response.Response({"success": "Thanks for upvoting"})

from rest_framework import generics, response, status, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .models import Post, Comment
from .serializers import PostsSerializer, CommentsSerializer, UpvotesSerializer


def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes
            # this call is needed for request permissions
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)
        return decorated_func
    return decorator


class IndexView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PostsSerializer
    queryset = Post.objects.all()

    @method_permission_classes((IsAuthenticatedOrReadOnly,))
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class NewsCommentsView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CommentsSerializer

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return Comment.objects.filter(news=post_id)

    @method_permission_classes((IsAuthenticatedOrReadOnly,))
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class NewsUpvoteView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = UpvotesSerializer

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return Post.objects.filter(pk=post_id).first()

    def put(self, request, *args, **kwargs):
        post_id = self.kwargs['pk']
        post = self.get_queryset()

        if not post:
            return response.Response({"error": "Such post does not exist"}, status=status.HTTP_404_NOT_FOUND)

        post.amount_of_upvotes += 1
        post.save(force_update=True)
        return response.Response({"success": "Thanks for upvoting"})

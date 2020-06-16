from django.urls import path
from .views import IndexView, AllCommentsView, NewsSubmitView, NewsCommentsView, NewsUpvoteView, NewsEditView, \
    CommentEditView

app_name = "news"

urlpatterns = [
    path('', IndexView.as_view()),
    path('submit', NewsSubmitView.as_view()),
    path('comments', AllCommentsView.as_view()),
    path('<int:news_pk>', NewsCommentsView.as_view()),
    path('<int:news_pk>/edit', NewsEditView.as_view()),
    path('<int:news_pk>/upvote', NewsUpvoteView.as_view()),
    path('<int:news_pk>/<int:comment_pk>', CommentEditView.as_view()),
]
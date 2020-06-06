from django.urls import path
from .views import IndexView, NewsCommentsView, NewsUpvoteView, NewsEditView

app_name = "news"

urlpatterns = [
    path('', IndexView.as_view()),
    path('<int:pk>', NewsCommentsView.as_view()),
    path('<int:pk>/upvote', NewsUpvoteView.as_view()),
]
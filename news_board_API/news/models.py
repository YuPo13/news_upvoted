from django.db import models
from django.utils.timezone import now


class Post(models.Model):
    title = models.TextField()
    link = models.TextField(unique=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(default=now)
    amount_of_upvotes = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return f'The news "{self.title}" (link: {self.link}) added by {self.author} on {self.creation_date} ' \
               f'is upvoted {self.amount_of_upvotes} times'


class Comment(models.Model):
    content = models.TextField()
    news = models.ForeignKey(Post, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(default=now)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return f'The comment "{self.content}" was added to news {self.news} by {self.author} on {self.creation_date}'
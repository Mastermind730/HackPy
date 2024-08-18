from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class News(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    hn_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    news = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.news.title}'




class CrawlHackerNews(models.Model):
    title = models.CharField(max_length=1000)
    link = models.URLField(max_length=1000)
    points = models.IntegerField(default=0)  # Provide a default value
    comments = models.IntegerField(default=0)  # Example field; adjust as needed
    date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=255, default='Anonymous')


    def __str__(self):
        return self.title


class Comment_Form(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Comment_Reply(models.Model):
    comment = models.ForeignKey(Comment_Form, related_name='replies', on_delete=models.CASCADE)
    reply = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.reply[:20]
class Vote(models.Model):
    VOTE_CHOICES = [
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(CrawlHackerNews, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('user', 'news')  # Each user can vote only once per news

    def __str__(self):
        return f'{self.user.username} voted {self.vote_type} on {self.news.title}'

class LinkSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



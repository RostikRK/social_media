from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass


class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    title = models.CharField(max_length=150)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "date": self.date_created,
            "likes": [user.username for user in self.likes.all()]
        }


class Following(models.Model):
    user_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")

    following_user_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    def serialize(self):
        return {
            "id": self.id,
            "follower": self.user_id.username,
            "following": self.following_user_id.username,
        }

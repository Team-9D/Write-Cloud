from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid

# Create your models here.

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.pk})


class Story(models.Model):

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    title = models.CharField(max_length=30)
    subtitle = models.CharField(max_length=60, default="")
    length = models.PositiveSmallIntegerField()

    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'story'
        verbose_name_plural = 'stories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('story_detail', kwargs={'pk': self.pk})


class Page(models.Model):

    number = models.IntegerField()
    content = models.TextField()

    story = models.ForeignKey('Story', on_delete=models.CASCADE)
    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'page'
        verbose_name_plural = 'pages'

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('page_detail', kwargs={'pk': self.pk})

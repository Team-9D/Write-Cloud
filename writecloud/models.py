from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
import os


# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="images/default-avatar.png", upload_to='images/')

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
    counter = models.IntegerField(default=0)
    subtitle = models.CharField(max_length=60, default="")
    length = models.PositiveSmallIntegerField()
    template = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(4), MinValueValidator(1)]
    )
    include_images = models.BooleanField(default=False)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')

    class Meta:
        verbose_name = 'story'
        verbose_name_plural = 'stories'

    def __str__(self):
        return f"{self.author}'s \"{self.title}\""

    def get_absolute_url(self):
        return reverse('story_detail', kwargs={'pk': self.pk})


class Page(models.Model):
    number = models.IntegerField()
    content = models.TextField(default="")
    image = models.ImageField(default=None)

    story = models.ForeignKey('Story', on_delete=models.CASCADE, related_name='pages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pages')

    class Meta:
        verbose_name = 'page'
        verbose_name_plural = 'pages'
        constraints = [
            models.UniqueConstraint(
                name='unique_story_author_page',
                fields=['story', 'author']
            ),
        ]

    def __str__(self):
        return f"{self.story} page {self.number} by {self.author}"

    def get_absolute_url(self):
        return reverse('page_detail', kwargs={'pk': self.pk})


class Review(models.Model):
    stars = models.IntegerField()
    body = models.TextField(default="")

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    story = models.ForeignKey('Story', on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
        constraints = [
            models.UniqueConstraint(
                name='unique_author_story_review',
                fields=['author', 'story']
            ),
        ]

    def __str__(self):
        return f"{self.story} reviewed by {self.author}"

    def get_absolute_url(self):
        return reverse('review_detail', kwargs={'pk': self.pk})

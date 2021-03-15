from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=30)

    profilepicture = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    bio = models.TextField()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.fullname

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"pk": self.pk})


class Story(models.Model):

    uuid = models.UUIDField()
    title = models.CharField(max_length=30)
    layout = models.CharField(max_length=30)
    length = models.PositiveSmallIntegerField()

    author = models.ForeignKey("UserProfile", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "story"
        verbose_name_plural = "stories"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("story_detail", kwargs={"pk": self.pk})


class Page(models.Model):

    number = models.IntegerField()
    banner = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    content = models.TextField()

    story = models.ForeignKey("Story", on_delete=models.CASCADE)
    author = models.ForeignKey("UserProfile", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "page"
        verbose_name_plural = "pages"

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("page_detail", kwargs={"pk": self.pk})

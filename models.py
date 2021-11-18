import urllib.parse as urlparse

from django.utils import timezone
from django.conf import settings

from django.db import models

from django.contrib import admin
from django.contrib.auth.models import User


# Create your models here.

class Resource(models.Model):

    def get_upload_filepath(instance, filename):
        return f"resources/{instance.user.id}/{instance.filename}"

    def get_file_path(a, b):
        return

    @admin.display(description="Public URL")
    def get_public_url(self):
        return f"{urlparse.urljoin(settings.MEDIA_URL, self.upload.name)}"

    # TODO: Validate that the authenticated user is the user in question or superuser.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #posts = models.ManyToManyField(Post, null=True)

    resource_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100, blank=True)

    # TODO: The URL should be unique for user, not unique for the whole database.
    filename = models.CharField(max_length=100, blank=False, unique=True)
    # file will be saved to MEDIA_ROOT/uploads/url
    upload = models.FileField(upload_to=get_upload_filepath)

    def __str__(self):
        return f"{self.description} @ {self.get_public_url()}"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post_id = models.AutoField(primary_key=True, blank=False)
    title = models.CharField(max_length=100, blank=False)
    url = models.CharField(max_length=100, blank=False, unique=True)
    # TODO: Unique URLs per date
    body = models.TextField(max_length=65536)
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)
    resources = models.ManyToManyField(Resource, null=True)
    hidden = models.BooleanField(default=False)
    summary = models.TextField(max_length=250, default='', blank=True, null=False)

    def __str__(self):
        return f"{self.title}, by {self.author}"

    def get_public_url(self):
        return f"/blog/{self.created_at.strftime('/%Y/%m/%d')}/{self.url}"

    def get_permalink(self):
        return f"/blog/posts/{self.url}"
    
    #@admin.display(description="User's resources")
    #def get_users_resources(self):
    #   return list(map(lambda x: f"{x.get_public_url()}, {x.description}", Resource.objects.filter(user=self.author)))
    
    def serialize(self):
        return {
            "author": str(self.author.username),
            "post_id": int(self.post_id),
            "title": self.title,
            "url": self.get_public_url(),
            "body": self.body,
            "published_at": self.published_at,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "summary": self.summary,
            "html": markdown.markdown(self.body),
        }

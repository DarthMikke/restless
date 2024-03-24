import markdown
import urllib.parse as urlparse
import os.path

from django.utils import timezone
from django.conf import settings
from django.urls import reverse

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


class ContentType(models.Model):
    """
    Base database object. Can get additional attributes by using Attributes
    objects.
    """
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post_id = models.AutoField(primary_key=True, blank=False)
    title = models.CharField(max_length=100, blank=False)
    # TODO: Unique URLs per date
    name = models.CharField(max_length=100, blank=False, unique=True)
    body = models.TextField(max_length=65536)
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)
    resources = models.ManyToManyField(Resource, blank=True)
    hidden = models.BooleanField(default=False)
    summary = models.TextField(max_length=250, default='', blank=True, null=False)

    class Meta:
        abstract = True

    content_type_id = None
    """
    Necessary to retrieve correct paths.
    """

    def __str__(self):
        return f"{self.title}, by {self.author}"

    def get_public_url(self):
        return os.path.join("/blog/", self.created_at.strftime('%Y/%m/%d'), self.name)
    
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


class ViewableContentType(ContentType):
    class Meta:
        abstract = True

    def get_summary(self):
        if len(self.summary) > 0:
            return markdown.markdown(self.summary)
        else:
            return markdown.markdown(self.body[:100]) + \
                ("…" if len(self.body > 100) else "")

    def html(self):
        return markdown.markdown(self.body)


class Post(ViewableContentType):
    content_type_id = "post"

    def get_permalink(self):
        return reverse('post', kwargs={
            "name": self.name
        })


class Page(ViewableContentType):
    content_type_id = "page"

    def get_permalink(self):
        return reverse('page', kwargs={"name": self.name})

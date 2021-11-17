from django.contrib import admin
from django import forms

from .models import Resource, Post

# Register your models here.


class ResourceInline(admin.TabularInline):
    model = Post.resources.through
    extra = 1


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('filename', 'user', 'description', 'get_public_url')

    # TODO: Only superusers can pick user – other users get a prefilled, non-editable field.


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
            {'fields': [
                'author',
                'title',
                'url',
                'body',
            ]}
        ),
        ('Resources',
            {'fields': ['resources'],
            'classes': ['extrapretty']
            }),
        ('Date information',
            {'fields': [
                'published_at',
                'created_at',
                'modified_at']
            }
        ),
    ]
#    inlines = [ResourceInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Resource, ResourceAdmin)

from django.urls import path
from .views import *

urlpatterns = [
    path('index/', get_index),
    path('posts/<str:posturl>', get_post),
    path('posts/<int:postid>', get_post_by_id),
    path('media/<int:resourceid>', get_resource),
]

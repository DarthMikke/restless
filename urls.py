from django.urls import path
from .views import *

urlpatterns = [
    #path('', get_index),
    path('api/index', index_api),
    path('rss.xml', get_rss),
    path('<int:year>/<int:month>/<int:day>/<str:post_url>', get_post),
    path('<int:year>/<int:month>/<int:day>/<str:post_url>/edit', edit_post),
    path('posts/<int:postid>', get_post_by_id),
    #path('media/<int:resourceid>', get_resource),
]

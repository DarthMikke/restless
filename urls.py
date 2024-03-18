from django.urls import path
from .views import *

urlpatterns = [
    path('', FrontPage.as_view()),
    path('api/index', index_api),
    path('rss.xml', get_rss),
    path('<int:year>/<int:month>/<int:day>/<str:name>', get_post),
    path('<int:year>/<int:month>/<int:day>/<str:name>/edit', edit_post),
    path('posts/<int:postid>', get_post_by_id),
    path('<str:name>', PageView.as_view()),
    #path('media/<int:resourceid>', get_resource),
]

from django.urls import path
from .views import *

urlpatterns = [
    path('', FrontPage.as_view()),
    path('api/index', index_api),
    path('rss.xml', get_rss),
    path('blog/<str:name>', PostView.as_view(), name='post'),
    path('<int:year>/<int:month>/<int:day>/<str:name>/edit', edit_post),
    path('posts/<int:postid>', get_post_by_id),
    path('<str:name>', PageView.as_view(), name='page'),
    #path('media/<int:resourceid>', get_resource),
]

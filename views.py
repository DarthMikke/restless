from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from restless.rest_additions.views import TemplateView
from .models import Page, Post, Resource

import markdown
import datetime

# Create your views here.

def index_api(request):
    posts_per_page = 10
    offset = 0
    if 'page' in request.GET.keys():
        offset = int(request.GET['page'])
    from_post = posts_per_page*offset
    to_post = posts_per_page*(offset + 1)

    posts = Post.objects.filter(hidden=False).order_by('-created_at')
    if from_post > len(posts):
        posts = []
    else:
        posts = [x.serialize() for x in posts[from_post:to_post]]
    response = {'total': len(posts), 'objects': posts}

    return JsonResponse(response)

def get_rss(request):
    ...

def get_post(request, year, month, day, post_url):
    posts = Post.objects.filter(url=post_url)
    print([(x.title, x.created_at, x.published_at) for x in posts])
    today = datetime.datetime(year, month, day, 0, 0)
    print(today)
    posts = list(filter(
        lambda x: x.created_at.timestamp() >= today.timestamp(),
        posts
    ))
    posts = list(filter(lambda x: x.created_at.timestamp() < (datetime.datetime(year, month, day, 0, 0) + datetime.timedelta(1)).timestamp(), posts))
    posts = list(filter(lambda x: x.published_at.timestamp() <= datetime.datetime.now().timestamp(), posts))

    if len(posts) > 1:
        return HttpResponse("Bad request", status=403)
    if len(posts) == 0:
        return HttpResponse("Not found", status=404)
    serialized = posts[0].serialize()
    return render(
        request,
        'restless/post.html',
        context={'post': serialized}
    )

def edit_post(request, year, month, day, post_url):
    ...

def get_post_by_id(request, postid):
    posts = Post.objects.filter(post_id=postid)

    if len(posts) > 1:
        return HttpResponse("Bad request", status=403)
    if len(posts) == 0:
        return HttpResponse("Not found", status=404)
    serialized = posts[0].serialize()
    serialized['html'] = markdown.markdown(serialized['body'])
    return render(
        request,
        'restless/post.html',
        context={'post': serialized}
    )

# Apache/Django will take care of this for now.
def get_resource(request, resource_id):
    ...


class FrontPage(TemplateView):
    model = Page
    template = "restless/page.html"
    identifiers = []

    def setup(self, *args, **kwargs):
        super().setup(self, *args, **kwargs)

        self.instance = self.model.objects.get(name='forside')

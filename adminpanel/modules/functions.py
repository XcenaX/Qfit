import json
from asgiref.sync import async_to_sync
import channels.layers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
COUNT_BLOG_ON_PAGE=50
from adminpanel.models import AdminUser

def get_paginated_blogs(request, paginator):
    page = request.GET.get('page')
    try:
        page = int(page)
    except:
        page = 1
    a = ""
    block = ""
    pages=[]
    if page:
        try:
            block = paginator.page(page)
        except EmptyPage:
            block = paginator.page(paginator.num_pages)
            page = paginator.num_pages

        for i in range(page-2, page+3):
            try:
                a = paginator.page(i)
                pages.append(i)
            except:
                continue
        print(pages)
        if pages[-1] != paginator.num_pages:
            pages.append(paginator.num_pages)

        if pages[0] != 1:
            pages.insert(0, 1)
    else:
        pages = [1,2,3,4,5,paginator.num_pages]
        block = paginator.page(1)
    return block, pages

def broadcast_ticks(ticks):
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)('timers', {
        'type': 'timers.message',
        "content": json.dumps(ticks),
    })

# Create your views here.
def get_parameter(request, name):
    try:
        return request.GET[name]
    except:
        return None 

def post_parameter(request, name):
    try:
        return request.POST[name]
    except:
        return None 

def post_file(request, name):
    try:
        return request.FILES.getlist(name)
    except:
        return None

def session_parameter(request, name):
    try:
        return request.session[name]
    except:
        return None

def get_current_user(request):
    if not request.session.get("user", None):
        return None
    user = AdminUser.objects.filter(id=int(request.session["user"])).first()
    return user

class make_incrementor(object):
    count = 0

    def __init__(self, start):
        self.count = start

    def inc(self, jump=1):
        self.count += jump
        return self.count

    def res(self):
        self.count = 0
        return self.count


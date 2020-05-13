from math import ceil  # 向上取整

from django.core.cache import cache
from django.shortcuts import render, redirect

from post.models import Post


# 主页
def post_list(request):
    page = int(request.GET.get('page', 1))  # 获取当前页
    per_page = 10  # 每一页10篇帖子
    start = (page - 1) * per_page  # 开始的文章
    end = start + per_page
    posts = Post.objects.all()[start:end]  # 每页显示的文章
    totale = Post.objects.all().count()  # 总文章数   django的orm中的指令，要熟悉d
    pages = ceil(totale / per_page)  # 总页数
    return render(request, 'post_list.html', {'posts': posts}, {'pages': range(pages)})


# 发贴
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(title=title, content=content)
        return redirect('/post/read/?post_id=%s' % post.id)
    return render(request, 'create_post.html')


# 修改帖子
def edit_post(request):
    if request.method == 'POST':
        post_id = int(request.POST.get('post_id'))
        post = Post.objects.get(pk=post_id)
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        # 更新缓存
        key = 'Post-%s' % post_id
        cache.set(key, post)
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        post_id = int(request.GET.get('post_id'))
        post = Post.objects.get(pk=post_id)
        return render(request, 'edit_post.html', {'post': post})


# 阅读帖子

def read_post(request):
    post_id = int(request.GET.get('post_id'))
    # 缓存
    key = 'Post-%s' % post_id
    post = cache.get(key)
    if post is None:
        post = Post.objects.get(pk=post_id)
        cache.set(key, post)

    return render(request, 'read_post.html', {'post': post})


# 删除帖子
def delete_post(request):
    post_id = int(request.GET.get('post_id'))
    Post.objects.get(pk=post_id).delete()
    return redirect('/')


def search(request):
    keyword = request.POST.get('keyword')
    posts = Post.objects.filter(content__contains=keyword)
    return render(request, 'search.html', {'posts': posts})

from django.core.cache import cache

from common import rds
from post.models import Post


# 页面缓存
def page_cache(timeout):
    def deco(view_func):
        def wrapper(request):
            key = 'PageCache-%s-%s' % (request.session.session_key, request.get_full_path())
            response = cache.get(key)
            if response is None:
                response = view_func(request)
                cache.set(key, response, timeout)
            return response
        return wrapper
    return deco


# 帖子阅读计数装饰器
def read_counter(read_view):
    def wrapper(request):
        response = read_view(request)
        # 状态码为 200 时计数
        if response.status_code == 200:
            post_id = int(request.GET.get('post_id'))
            rds.zincrby('ReadRank', 1, post_id)
        return response
    return wrapper


# 获取帖子排行前 N 的数据
def get_top_n(num):

    # ori_data = [
    #     (b'39', 369.0),
    #     (b'26', 301.0),
    #     (b'60', 230.0),
    # ]
    ori_data = rds.zrevrange('ReadRank', 0, num-1, withscores=True)

    # 数据清洗
    # cleaned = [
    #     [39, 369],
    #     [26, 301],
    #     [60, 230],
    # ]
    cleaned = [[int(post_id), int(count)] for post_id, count in ori_data]
    # 方法一
    # post_id_list = [post_id for post_id, _ in cleaned]  # 取出 post_id 列表
    # posts = Post.objects.filter(id__in=post_id_list)  # 根据 id 批量获取post
    # posts = sorted(posts, key=lambda post:post_id_list.index(post.id))  # 根据 id 位置排序
    # for post, item in zip(posts, cleaned):
    #     item[0] = post # 逐个替换 post

    post_id_list = [post_id for post_id, _ in cleaned]  # 批量获取 post
    posts = Post.objects.in_bulk(post_id_list)
    for item in cleaned:
        item[0] = posts[item[0]]
    return cleaned
from time import time

from django.shortcuts import render

from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin


class BlockSpiderMiddleware(MiddlewareMixin):
    # 限制访问频率中间件： 最高频率为 3 次/秒
    def process_request(self, request):
        user_ip = request.META['REMOTE_ADDR']

        request_key = 'Request-%s' % user_ip  # 用户请求时间的 key
        block_key = 'Block-%s' % user_ip      # 被封禁用户的 key

        if cache.get(block_key):
            return render(request, 'blockers.html')

        # 取出当前时间，历史访问时间
        now = time.time()
        request_history = cache.get(request_key, [0] * 3)

        # 检查与最早访问时间的间隔
        if now - request_history.pop(0) >= 1:
            request_history.append(now)
            cache.set(request_key, request_history)
            return
        else:
            # 访问超过限制，将用户 IP 加入缓存
            cache.set(block_key, 1, 86400)  # 封禁用户 24 小时
            return render(request, 'blockers.html')
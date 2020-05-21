from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=64)  # 帖子标题
    created = models.DateTimeField(auto_now_add=True)  # 发帖时间
    content = models.TextField()  # 贴子内容
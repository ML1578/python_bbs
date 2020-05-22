from django.db import models

from user.models import User


class Post(models.Model):
    uid = models.IntegerField()
    title = models.CharField(max_length=64)  # 帖子标题
    created = models.DateTimeField(auto_now_add=True)  # 发帖时间
    content = models.TextField()  # 贴子内容

    @property
    def auth(self):
        if not hasattr(self, '_auth'):
            self._auth = User.objects.get(id=self.uid)
        return self._auth
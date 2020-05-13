from django.db import models


class User(models.Model):
    SEX = (
        ('M', '男性'),
        ('F', '女性'),
        ('S', '保密'),
    )  # 限制性别
    nickname = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=128)
    icon = models.ImageField()
    plt_icon = models.CharField(max_length=256, blank=True) # 第三方平台用户的头像
    age = models.IntegerField(default=18)
    sex = models.CharField(max_length=8, choices=SEX)

    @property
    def get_avatar(self):
        return self.icon.url if self.icon else self.plt_icon

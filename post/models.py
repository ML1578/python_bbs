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

    # 帖子的所有评论
    def comments(self):
        return Comment.objects.filter(post_id=self.id).order_by('-id')

    # 帖子对应的所有 tag
    def tags(self):
        relations = PostTagRelation.objects.filter(post_id=self.id).only('tag_id')  # 取出post与tag的关系
        tag_id_list = [r.tag_id for r in relations]  # 取出对应的tag id 列表
        return Tag.objects.filter(id__in=tag_id_list)  # 返回对应的 tag

    # 更新 post 对应的 tag
    def update_tags(self, tag_names):
        updated_tags = set(Tag.ensure_tags(tag_names))
        current_tags = set(self.tags())

        # 找出尚未关联的 tag
        need_create_tags = updated_tags - current_tags
        need_create_tag_id_list = [t.id for t in need_create_tags]
        PostTagRelation.add_relations(self.id, need_create_tag_id_list)

        # 找出需要删除关联的 tag
        need_delete_tags = current_tags - updated_tags
        need_delete_tag_id_list = [t.id for t in need_delete_tags]
        PostTagRelation.del_relations(self.id, need_delete_tag_id_list)


class Comment(models.Model):
    uid = models.IntegerField()
    post_id = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    @property
    def auth(self):
        if not hasattr(self, '_auth'):
            self._auth = User.objects.get(id=self.uid)
        return self._auth

    @property
    def post(self):
        if not hasattr(self, '_post'):
            self._post = User.objects.get(id=self.post_id)
        return self._post


# post 与 tag 的关系表
class PostTagRelation(models.Model):
    post_id = models.IntegerField()
    tag_id = models.IntegerField()

    # 建立 post id 与 tags 的对应关系
    @classmethod
    def add_relations(cls, post_id, tag_id_list):
        new_relations = [cls(post_id=post_id, tag_id=tid) for tid in tag_id_list]
        cls.objects.bulk_create(new_relations)

    @classmethod
    def del_relations(cls, post_id, tag_id_list):
        cls.objects.filter(post_id=post_id, tag_id__in=tag_id_list).delete()


class Tag(models.Model):
    name = models.CharField(max_length=16, unique=True)

    # 确保传入的 tag 已存在, 如果不存在直接创建出来
    @classmethod
    def ensure_tags(cls, tag_names):
        exists = cls.objects.filter(name__in=tag_names)
        exist_names = set(t.name for t in exists)    # 已存在的 tag 的 name
        new_names = set(tag_names) - exist_names     # 待创建的 tag 的 name
        new_tags = [cls(name=n) for n in new_names]  # 待创建的 tag
        cls.objects.bulk_create(new_tags)            # 批量提交创建
        return cls.objects.filter(name__in=tag_names)

    # 当前 tag 对应的所有 post
    def posts(self):
        relations = PostTagRelation.objects.filter(tag_id=self.id).only('post_id')  # 取出tag与post的关系
        post_id_list = [r.post_id for r in relations]  # 取出对应的post id 列表
        return Post.objects.filter(id__in=post_id_list)  # 返回对应的 post
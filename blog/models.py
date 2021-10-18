from django.db import models
from django.contrib.auth.models import AbstractUser
from tinymce.models import HTMLField

# Create your models here.


#用户
class UserProfile(AbstractUser):

    gender = (
        ('male', "男"),
        ('female', "女")
    )

    username = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="male")
    create_time = models.DateTimeField(auto_now_add=True)
    hobby = models.TextField()
    # display = models.IntegerField('是否展示自己的文章', default=0)


    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural=verbose_name = '用户信息'


#文章类别
class Category(models.Model):
    name = models.CharField('类别名', max_length=20, unique=True)

    class Meta:
        verbose_name_plural = verbose_name = '类别名'

    def __str__(self):
        return self.name


#文章标签
class Tag(models.Model):
    name = models.CharField('标签', max_length=20, unique=True)

    class Meta:
        verbose_name_plural = verbose_name ='标签'

    def __str__(self):
        return self.name


#文章
class Article(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, verbose_name='作者')
    title = models.CharField('标题', max_length=50)
    content = models.TextField('内容') # '<html><body><h1>标题一</h1></body></html>'
    pub_time = models.DateTimeField('创建日期', auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='类别', null=True, blank=True)
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    visitor = models.IntegerField('访问量', default=0)
    discuss = models.BooleanField('是否允许别人评论', default=True)
    display = models.BooleanField('是否展示自己的文章', default=True)

    class Meta:
        verbose_name_plural = verbose_name = '文章'

    def __str__(self):
        return self.title


#评论
class Comment(models.Model):
    # name = models.CharField('昵称', max_length=20)
    # email = models.EmailField('邮箱')
    content = models.TextField('内容')
    created = models.DateField('时间', auto_now=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='文章')
    name = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='评论人')
    # reply = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='回复')
    undiscuss = models.BooleanField('未处理评论', default=True)


    class Meta:
        verbose_name_plural = verbose_name = '评论'

    def __str__(self):
        return self.content

# 测试git
#评论回复
class CommentReply(models.Model):
    content = models.TextField('内容')
    created = models.DateField('时间', auto_now=True)
    # article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='文章')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='评论')
    reply_user = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='回复人',
        related_name='reply_user'
    )
    comment_user = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='被回复人',
        related_name='comment_user'
    )
    unreply = models.BooleanField('未处理回复', default=True)

    class Meta:
        verbose_name_plural = verbose_name = '评论回复'

    def __str__(self):
        return self.content




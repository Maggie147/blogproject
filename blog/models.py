#coding:utf-8
from django.db import models

# coding:utf-8
# Create your models here.
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse
import markdown
from django.utils.html import strip_tags


# 分类
@python_2_unicode_compatible
class Category(models.Model):
	# name字段, 储存分类名称
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name


# 标签
@python_2_unicode_compatible
class Tag(models.Model):
	# name字段, 储存标签名称
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name


# 文章
@python_2_unicode_compatible
class Post(models.Model):
	# 文章标题, 正文
	title = models.CharField(max_length=70)
	body = models.TextField()

	# 创建时间, 修改时间
	created_time = models.DateTimeField()
	modified_time = models.DateTimeField()

	# 摘要 (默认情况下 CharField 要求我们必须存入数据,否则就会报错; CharField 的 blank=True 参数值后就可以允许空值了)
	excerpt = models.CharField(max_length=200, blank=True)

	# 分类,标签 (ForeignKey，即一对多的关联; ManyToManyField，表明这是多对多的关联)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	tags = models.ManyToManyField(Tag, blank=True)

	# 文章作者 (从 django.contrib.auth.models 导入的, Django内置的应用,专门用于处理网站用户的注册、登录等流程的用户模型)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	# views字段 记录阅读量
	views = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.title

	''' reverse函数, 第一个参数 'blog:detail', 表 blog 应用下的 name=detail 的视图函数。
	于是 reverse 函数会去解析 detail视图函数对应的 URL,  detail 对应的规则 'post/<int:pk>/'。
	如果 Post 的 id是 666, 那么 get_absolute_url 函数返回的就是 /post/666/, 这样 Post 自己就生成了自己的 URL。
	'''
	def get_absolute_url(self):
		return reverse('blog:detail', kwargs = {'pk':self.pk})


	def save(self, *args, **kwargs):
		if not self.excerpt:
			md = markdown.Markdown(extensions=[
				'markdown.extensions.extra',
				'markdown.extensions.codehilite',
				])
			self.excerpt = strip_tags(md.convert(self.body)[:54])
			super(Post, self).save(*args, **kwargs)

	def increase_views(self):
		self.views += 1
		self.save(update_fields=['views'])

	# Meta 类 的 ordering 属性, 指定默认排序方式
	class Meta:
		ordering = ['-created_time', 'title']
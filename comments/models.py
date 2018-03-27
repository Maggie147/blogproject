from django.db import models

# Create your models here.

from django.utils.six import python_2_unicode_compatible

@python_2_unicode_compatible
class Comment(models.Model):
	# 名字
	name = models.CharField(max_length=100)
	# 邮箱
	email = models.EmailField(max_length=255)
	# 个人网站
	url = models.URLField(blank=True)
	# 评论内容
	text = models.TextField()
	# 评论时间
	created_time = models.DateTimeField(auto_now_add=True)


	post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)

	def __str__(self):
		return self.text[:20]
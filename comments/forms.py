from django import forms
from .models import Comment

'''
表单的内部类 Meta:
models = Comment 表这个表单对应的数据库模型是 Comment 类
fields = ['name', 'email', 'url', 'text'] 指定了表单需要显示的字段
'''
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['name', 'email', 'url', 'text']
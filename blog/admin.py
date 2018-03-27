# Register your models here.

from django.contrib import admin
from .models import Post, Category, Tag



'''定制Admin, 将在admin post 列表显示更加详细的信息。
'''
class PostAdmin(admin.ModelAdmin):
	list_display = ['title', 'created_time', 'modified_time', 'category', 'author']

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
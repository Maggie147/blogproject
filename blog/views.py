#coding:utf-8
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import Post, Category
import markdown

def index(request):
	# return HttpResponse("欢迎访问我的博客首页！")

	post_list = Post.objects.all().order_by('-created_time')

	template = loader.get_template('blog/index.html')
	# context = {
	# 'title': '我的博客首页',
	# 'welcome': '欢迎访问我的博客首页'
	# }
	context = {
	'post_list': post_list
	}

	# return HttpResponse(template.render(context, request))
	return render(request, 'blog/index.html', context)



def detail(request, pk):
	post = get_object_or_404(Post, pk=pk)

	post.body = markdown.markdown(post.body,
		extensions =[
		'markdown.extensions.extra',
		'markdown.extensions.codehilite',
		'markdown.extensions.toc',
		])
	return render(request, 'blog/detail.html', context={'post':post})


def archives(request, year, month):
	post_list = Post.objects.filter(
		created_time__year = year,
		created_time__month = month
		).order_by('-created_time')

	return render(request, 'blog/index.html', context={'post_list':post_list})

def category(request, pk):
	cate = get_object_or_404(Category, pk=pk)
	post_list = Post.objects.filter(category=cate).order_by('-created_time')
	return render(request, 'blog/index.html', context={'post_list':post_list})
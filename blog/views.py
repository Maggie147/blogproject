#coding:utf-8
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import Post, Category
import markdown

from django.views.generic import ListView
from django.db.models import Q

class IndexView(ListView):
	model = Post
	template_name = "blog/index.html"
	context_object_name = 'post_list'
	paginate_by = 2

	def get_context_date(self, **kwargs):
		# 首先获得父类生成的传递给模板的字典。
		context = super().get_context_date(**kwargs)
		# 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量

		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')
		# 调用 pagination_data 方法获得显示分页导航条需要的数据
		pagination_data = self.pagination_data(paginator, page, is_paginated)
		# 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典
		context.update(pagination_data)

		return context

	def pagination_data(self, paginator, page, is_paginated):
		# 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
		if not is_paginated:
			return {}
		left = []

		right = []

		left_has_more = False
		right_has_more = False

		first = False
		last = False

		page_number = page.number

		total_pages = paginator.num_pages

		page_range = paginator.page_range

		if page_number == 1:
			right = page_range[page_number: page_number+2]

			if right[-1] < total_pages -1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True

		elif page_number == total_pages:
			left = page_range[(page_number - 3) if (page_number -3) > 0 else 0: page_number -1]

			if left[0] >2:
				left_has_more = True
			if left[0] >1:
				first = True
		else:
			left = page_range[(page_number -3) if (page_number -3) > 0 else 0: page_number -1]
			right = page_range[page_number: page_number +2]

			if right[-1] < total_pages -1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True
			if left[0] > 2:
				left_has_more = True
			if left[0] >1:
				first = True


		data = {
		'left':left,
		'right':right,
		'left_has_more':left_has_more,
		'right_has_more':right_has_more,
		'first':first,
		'last':last,
		}
		return data

def index(request):
	post_list = Post.objects.all()
	return render(request, 'blog/index.html', context={'post_list':post})


# def index(request):

# 	post_list = Post.objects.all().order_by('-created_time')

# 	template = loader.get_template('blog/index.html')
# 	context = {
# 	'post_list': post_list
# 	}

# 	# return HttpResponse(template.render(context, request))
# 	return render(request, 'blog/index.html', context)



def detail(request, pk):
	post = get_object_or_404(Post, pk=pk)

	# 阅读量 +1
	post.increase_views()

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

# def category(request, pk):
# 	cate = get_object_or_404(Category, pk=pk)
# 	post_list = Post.objects.filter(category=cate).order_by('-created_time')
# 	return render(request, 'blog/index.html', context={'post_list':post_list})

class CategoryView(IndexView):
	def get_queryset(self):
		cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
		return super(CategoryView, self).get_queryset().filter(category=cate)

class TagView(ListView):
	model = Post
	template_name = "blog/index.html"
	context_object_name = "post_list"

	def get_queryset(self):
		tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))

		return super(TagView, self).get_queryset().filter(tags=tag)

def search(request):
	q = request.GET.get('q')
	error_msg = ''

	if not q:
		error_msg = "请输入关键词"
		return render(request, 'blog/index.html', {'error_msg':error_msg})

	post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
	return render(request, 'blog/index.html', context={'post_list': post_list})

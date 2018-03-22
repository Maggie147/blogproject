from django.urls import path, re_path
from . import views

app_name = 'blog'
urlpatterns = [
    re_path('^$', views.index, name='index'),
    # re_path('.*?index.html', views.index,),
    # path('^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    path('post/<int:pk>/', views.detail, name='detail'),
    path('archives/<int:year>/<int:month>', views.archives, name='archives'),
    path('category/<int:pk>/', views.category, name='category'),
]
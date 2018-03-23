# blogproject
基于最新版 Django 2.0 和 Python 3.5.4

## 资源列表
-
-
-
-

1. 克隆项目到本地

   打开命令行，进入到保存项目的文件夹，输入如下命令：

   ```
   git clone https://github.com/TXxue/blogproject.git
   ```

2. 创建并激活虚拟环境

   在命令行进入到保存虚拟环境的文件夹，输入如下命令创建并激活虚拟环境：

   ```
   virtualenv blogproject_env

   # windows
   blogproject_env\Scripts\activate

   # linux
   source blogproject_env/bin/activate
   ```

   关于如何使用虚拟环境，参阅：[搭建开发环境](http://zmrenwu.com/post/3/) 的 Virtualenv 部分。如果不想使用虚拟环境，可以跳过这一步。

3. 安装项目依赖

   如果使用了虚拟环境，确保激活并进入了虚拟环境，在命令行进入项目所在的 django-blog-tutorial 文件夹，运行如下命令：

   ```
   pip install -r requirements.txt
   ```

4. 迁移数据库

   在上一步所在的位置运行如下命令迁移数据库：

   ```
   python manage.py migrate
   ```

5. 创建后台管理员账户

   在上一步所在的位置运行如下命令创建后台管理员账户

   ```
   python manage.py createsuperuser
   ```

   具体请参阅 [在 Django Admin 后台发布文章](http://zmrenwu.com/post/9/)

6. 运行开发服务器

   在上一步所在的位置运行如下命令开启开发服务器：

   ```
   python manage.py runserver
   ```

   在浏览器输入：127.0.0.1:8000


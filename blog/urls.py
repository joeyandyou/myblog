from django.urls import path
from . import views

urlpatterns = [
    # 主页
    path('index/', views.index),

    #未登录主页
    path('unindex/', views.unindex),

    # 登录
    path('login/', views.tologin),

    # 注册
    path('register/', views.register),

    # 注销
    path('logout/', views.lagout),

    #个人信息
    path('person/', views.person),

    #个人文章列表
    path('article_list/', views.article_list),

    #新增文章
    path('add_article/', views.add_article),

    #文章详情
    path('detail_article/', views.detail_article),

    #修改文章
    path('edit_article/', views.edit_article),

    #删除文章
    path('del_article/', views.del_article),

    #回复评论
    path('reply_comment/', views.reply_comment),

    #评论中心
    path('comment_center/', views.comment_center),

    #评论中心
    path('reply_center/', views.reply_center),

    #模板评论中心回复数量
    #path('base.html/', views.base)

    #用户添加评论
    #path('add_user_comment/', views.add_user_comment),


    #作者删除评论
    #path('del_comment/', views.del_comment),



]
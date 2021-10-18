import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from blog import models
# Create your views here.
from .models import UserProfile, Article, Comment, CommentReply, Tag, Category
from django.db.models import Q




#登录
def tologin(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            data = request.POST
            username = data.get("username")
            password = data.get("password")
            n = authenticate(username=username, password=password)
            if n:
                login(request, user=n)
                return redirect('/index/')
        else:
            return render(request, 'login.html')
    else:

        return redirect('/index/')


#注册
def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            data = request.POST
            username = data.get('username')
            #print('sex:', sex)

            if not username:
                message = '用户名不能为空！'
                return render(request, 'ERROR.html', {'message': message})
            else:
                password = data.get('password')
                password1 = data.get('password1')
                if password1 == password:
                    email = data.get('email')
                    sex = data.get('sex')
                    create_time = data.get('create_time')
                    hobby = data.get('hobby')
                    u = UserProfile.objects.filter(username=username).first()
                    e = UserProfile.objects.filter(email=email).first()
                    if u:
                        message = "该用户名已被注册"
                        return render(request, 'ERROR.html', {'message': message})
                    elif e:
                        message = "该邮箱已被注册"
                        return render(request, 'ERROR.html', {'message': message})
                    else:
                        UserProfile.objects.create_user(
                            username=username,
                            password=password,
                            email=email,
                            sex=sex,
                            create_time=create_time,
                            hobby=hobby
                        )
                        return redirect('/login/')

                else:
                    message = '请确认输入的密码一致！'
                    return render(request, 'ERROR.html', {'message': message})
        else:
            return render(request, 'register.html')

    else:
        info = '您已登录！！已为你注销！请再次注册！'
        logout(request)
        return render(request, 'register.html', {'info': info})


#注销
def lagout(request):
    if not request.user.is_authenticated:
        message = '您还未登录！'
        return redirect('/login/')
    else:
        logout(request)
        return redirect('/unindex/')


#未登录主页
def unindex(request):
    if request.user.is_authenticated:
        return redirect('/index/')
    a = models.Article.objects.filter(display=True).order_by('-visitor')[:5]
    # 按时间
    b = models.Article.objects.all().order_by('-pub_time')
    paginator = Paginator(a, 5)
    # print('-'*30)
    # print(paginator.page_range)
    page_nums = list(paginator.page_range)
    # print(page_nums)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)

    except PageNotAnInteger:
        contacts = paginator.page(1)

    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'unindex.html', {"current": 'index', 'contacts': contacts, 'page_nums': page_nums})


#个人信息
def person(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    p = request.user
    if request.method == 'POST':

        # 1 提取参数
        username = request.POST.get("username")
        email = request.POST.get("email")
        sex = request.POST.get("sex")
        hobby = request.POST.get("hobby")
        #display = request.POST.get("display")

        # u = UserProfile.objects.filter(username=username).first()
        # e = UserProfile.objects.filter(email=email).first()
        # if u:
        #     if u != p:
        #         message = '用户名已经被使用'
        #         return render(request, 'ERROR.html', {'message': message})
        #
        # models.UserProfile.objects.filter(id=p.id).update(username=username)

        # 2 检查参数是否可用（检查username、email是否被使用）,检查不通过 -> 返回错误提示
        u = UserProfile.objects.filter(username=username).exclude(id=p.id).first()
        if u:
            message = '用户名已经被使用'
            return render(request, 'ERROR.html', {'message': message})
        e = UserProfile.objects.filter(email=email).exclude(id=p.id).first()
        if e:
            message = '邮箱已经被使用'
            return render(request, 'ERROR.html', {'message': message})

        # 3 检查通过 -> 修改
        # models.UserProfile.objects.filter(id=p.id).update(sex=sex, hobby=hobby, username=username, email=email)
        p.username = username
        p.email = email
        p.sex = sex
        p.hobby = hobby
        #p.display = display
        p.save()

        return redirect('/person/')




        # if username and email and sex and hobby:
        #     u = UserProfile.objects.filter(username=username).first()
        #     e = UserProfile.objects.filter(email=email).first()
        #     print("是什么")
        #     print(e)
        #     print(p.email)
        #     print(e == p.email)

        #     # if str(u) == str(p.username):
        #     if u.username == p.username:
        #         if e.email == p.email:
        #             models.UserProfile.objects.filter(id=p.id).update(sex=sex, hobby=hobby)
        #             return redirect('/person/')
        #         else:
        #             models.UserProfile.objects.filter(id=p.id).update(email=email, sex=sex, hobby=hobby)
        #             return redirect('/person/')
        #     elif str(e) == str(p.email):
        #         models.UserProfile.objects.filter(id=p.id).update(username=username, sex=sex, hobby=hobby)
        #         return redirect('/person/')
        #     elif u:
        #         message = "该用户名已被使用"
        #         return render(request, 'ERROR.html', {'message': message})
        #     elif e:
        #         message = "该邮箱已被使用"
        #         return render(request, 'ERROR.html', {'message': message})
        #     else:
        #
        #         models.UserProfile.objects.filter(id=p.id).update(username=username, email=email, sex=sex, hobby=hobby)
        #         return redirect('/person/')
        #
        # else:
        #     message = '输入的信息不能为空'
        #     return render(request, 'ERROR.html', {'message': message})
    return render(request, "personal.html", {'p': p, "current": 'person', 'count': census(request)})

#修改个人基本信息
'''def edit_person(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    id = request.POST.get("id")

    #plisher_obj = models.UserProfile.objects.filter(id=id)

    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        sex = request.POST.get("sex")
        hobby = request.POST.get("hobby")
        models.UserProfile.objects.filter(id=id).update(username=username, email=email, sex=sex, hobby=hobby)
        return redirect('/person/')

    return render(request, 'edit_person.html')'''


#我的文章列表
def article_list(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    user = request.user
    a = Article.objects.filter(author=request.user).order_by('-pub_time')
    b = a.all().first().id
    print("*"*20)
    print(b)
    paginator = Paginator(a, 5)
    #print('-'*30)
    #print(paginator.page_range)
    page_nums = list(paginator.page_range)
    #print(page_nums)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)

    except PageNotAnInteger:
        contacts = paginator.page(1)

    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'article_list.html', {'contacts': contacts, "current": 'article_list', 'user': user,
                                                 'page_nums': page_nums, 'count': census(request)})


#撰寫文章
def add_article(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    p = request.user
    category = models.Category.objects.all()
    if request.method == 'POST':
        data = request.POST
        if data.get("title") and data.get("content"):
            title = data.get("title")
            content = data.get("content")
            pub_time = datetime.datetime.now()
            display = data.get("display")
            category1 = models.Category.objects.filter(name=data.get("category")).first()
            models.Article.objects.create(author=p, title=title, content=content, pub_time=pub_time, display=display, category=category1)
            return redirect('/article_list/')
        else:
            message = '输入信息不能为空'
            return render(request, 'ERROR.html', {'message': message})
    return render(request, 'add_article.html', {'p': p, "current": 'article_list', 'category': category,
                                                'count': census(request)})


#修改文章
def edit_article(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    article_id = request.GET.get("article_id")
    article = models.Article.objects.filter(id=article_id).first()
    models.Article.objects.filter(id=article_id).update(visitor=article.visitor+1)
    user = request.user
    if request.method == 'POST':
        data = request.POST
        title = data.get("title")
        display = data.get("display")
        discuss = data.get("discuss")
        #print(title)
        #print(11111111123154)
        content = data.get("content")
        models.Article.objects.filter(id=article_id).update(title=title, content=content, display=display, discuss=discuss)
        return redirect("/article_list/")
    return render(request, "edit_article.html", {'user': user, 'article': article, "current": 'article_list',
                                                 'count': census(request)})


#主页
def index(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    category = models.Category.objects.all()
    if request.method == 'POST':
        key = request.POST.get('key')
        select = request.POST.get('type')
        name = request.POST.get('category')
        list1 = []
        if request.POST.get('a'):
            list1.append(request.POST.get('a'))
        if request.POST.get('b'):
            list1.append(request.POST.get('b'))
        if request.POST.get('c'):
            list1.append(request.POST.get('c'))
        if request.POST.get('d'):
            list1.append(request.POST.get('d'))
        if list1:

            a = len(list1)

            #a = len(list1)
            article = models.Article.objects.filter(tag=list1[a-1])
            paginator_search = Paginator(article, 5)
            page_nums = list(paginator_search.page_range)
            page_search = request.GET.get('page')
            try:
                contacts = paginator_search.page(page_search)

            except PageNotAnInteger:
                contacts = paginator_search.page(1)

            except EmptyPage:
                contacts = paginator_search.page(paginator_search.num_pages)
            return render(request, 'search.html', {"current": 'index', 'article1': article, 'contacts': contacts,
                                                       'page_nums': page_nums, 'category': category,
                                                       'count': census(request)})

        if name:
            category_search = Category.objects.filter(name=name).first()
            article = category_search.article_set.all()
            paginator_search = Paginator(article, 5)
            page_nums = list(paginator_search.page_range)
            page_search = request.GET.get('page')
            try:
                contacts = paginator_search.page(page_search)

            except PageNotAnInteger:
                contacts = paginator_search.page(1)

            except EmptyPage:
                contacts = paginator_search.page(paginator_search.num_pages)
            return render(request, 'search.html', {"current": 'index', 'article1': article, 'contacts': contacts,
                                                   'page_nums': page_nums, 'category': category,
                                                   'count': census(request)})
        if key:
            if select == '1':
                article = models.Article.objects.filter(title__contains=key, display=True).order_by('-pub_time')
                paginator_search = Paginator(article, 5)
                page_nums = list(paginator_search.page_range)
                page_search = request.GET.get('page')
                try:
                    contacts = paginator_search.page(page_search)

                except PageNotAnInteger:
                    contacts = paginator_search.page(1)

                except EmptyPage:
                    contacts = paginator_search.page(paginator_search.num_pages)
                return render(request, 'search.html', {"current": 'index', 'article1': article, 'contacts': contacts,
                                                       'page_nums': page_nums, 'category': category, 'count': census(request)})
            elif select == '2':
                article = models.Article.objects.filter(content__contains=key, display=True).order_by('-pub_time')
                paginator_search = Paginator(article, 5)
                page_nums = list(paginator_search.page_range)
                # print(page_nums)
                page_search = request.GET.get('page')
                try:
                    contacts = paginator_search.page(page_search)

                except PageNotAnInteger:
                    contacts = paginator_search.page(1)

                except EmptyPage:
                    contacts = paginator_search.page(paginator_search.num_pages)
                return render(request, 'search.html', {"current": 'index', 'article1': article, 'contacts': contacts,
                                                       'page_nums': page_nums, 'category': category})
            elif select == '3':
                user = models.UserProfile.objects.filter(username__contains=key).first()
                article = models.Article.objects.filter(author=user, display=True)
                paginator_search = Paginator(article, 5)
                page_nums = list(paginator_search.page_range)
                # print(page_nums)
                page_search = request.GET.get('page')
                try:
                    contacts = paginator_search.page(page_search)

                except PageNotAnInteger:
                    contacts = paginator_search.page(1)

                except EmptyPage:
                    contacts = paginator_search.page(paginator_search.num_pages)
                return render(request, 'search.html', {"current": 'index','article1': article, 'contacts': contacts,
                                                       'page_nums': page_nums, 'category': category, 'count': census(request)})

    # users = models.UserProfile.objects.all().exclude(display=False)
    #users = models.UserProfile.objects.filter(display=True)
    # 按热度
    a = models.Article.objects.filter(display=True).order_by('-visitor')
    #按时间
    b = models.Article.objects.all().order_by('-pub_time')
    paginator = Paginator(a, 5)
    # print('-'*30)
    # print(paginator.page_range)
    page_nums = list(paginator.page_range)
    #print(page_nums)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)

    except PageNotAnInteger:
        contacts = paginator.page(1)

    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {"current": 'index', 'contacts': contacts, 'page_nums': page_nums,
                                          'category': category, 'count': census(request)})


#刪除文章
def del_article(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    article_id = request.GET.get("article_id")
    models.Article.objects.filter(id=article_id).delete()
    return redirect('/article_list/', {'count': census(request)})


#文章详情
def detail_article(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    article_id = request.GET.get("article_id")
    essay = Article.objects.filter(id=article_id).first()
    models.Article.objects.filter(id=article_id).update(visitor=essay.visitor + 1)
    discuss = Comment.objects.filter(article=essay)
    discuss_list = []
    for discuss1 in discuss:
        # reply_all = CommentReply.objects.filter(comment=discuss1)
        #反向查询
        reply_all = discuss1.commentreply_set.all()
        discuss_list.append({'comment': discuss1, 'reply1': reply_all})

    data = request.POST
    content = data.get("comment")#找到提交的评论内容
    comment_id = data.get("comment_id")  # 拿到提交评论的id
    user = request.user#当前用户
    reply = data.get("reply")#内容
    if request.method == 'POST':
        if content:
            time = datetime.datetime.now()
            models.Comment.objects.create(content=content, created=time, article=essay, name=user)

        elif comment_id:
            pinglun = Comment.objects.filter(id=comment_id).first()
            models.Comment.objects.filter(id=comment_id).update(undiscuss=False)
            time = datetime.datetime.now()

            models.CommentReply.objects.create(content=reply, created=time, comment=pinglun, reply_user=user,
                                               comment_user=pinglun.name)
    return render(request, 'detail_article.html', {'essay': essay, "current": 'article_list',
                                                   'discuss_list': discuss_list, 'user': user, 'count': census(request)})


#评论中心
def comment_center(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    user = request.user
    article = models.Article.objects.filter(author=user).all()
    list1 = []
    for i in article:
        comment = models.Comment.objects.filter(undiscuss=True, article=i).all().order_by('-created')
        for a in comment:
            list1.append(a)
    if request.method == 'POST':
        comment_id = request.POST.get("comment_id")
        models.Comment.objects.filter(id=comment_id).update(undiscuss=False)
    return render(request, 'comment_center.html/', {'list1': list1, 'count': census(request)})


#回复中心
def reply_center(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    user = request.user
    article = models.Article.objects.filter(author=user).all()
    list1 = []
    for i in article:
        comment = models.Comment.objects.filter(article=i).all().order_by('-created')
        for a in comment:
            reply_all = a.commentreply_set.filter(unreply=True).all()
            list1.append({'comment': a, 'reply1': reply_all})
    if request.method == 'POST':
        comment_id = request.POST.get("reply_comment_id")
        models.CommentReply.objects.filter(id=comment_id).update(unreply=False)
    return render(request, 'reply_center.html/', {'list1': list1, 'count': census(request)})
# 测试git

#主页统计未处理评论与回复数量
def census(request):
    user = request.user
    article = models.Article.objects.filter(author=user).all()
    chen = 0
    dan = 0
    for i in article:
        comment = models.Comment.objects.filter(undiscuss=True, article=i).all()
        a = len(comment)
        chen = chen+a
        for c in comment:
            b = len(models.CommentReply.objects.filter(unreply=True, comment=c).all())
            dan = dan+b
    count1 = chen+dan
    return count1


#回復評論
def reply_comment(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    id1 = request.GET.get("article_id")
    print(id1)
    return render(request, 'reply_comment.html', {'id1': id1, 'count': census(request)})


#作者刪除評論
def del_comment(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    pass



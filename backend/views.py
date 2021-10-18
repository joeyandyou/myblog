import datetime
import json
import os

from django.contrib.auth.hashers import make_password
from django.db.models import Q, Sum, Count
from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from backbone import models as bbm
from django.contrib import auth
from django import forms
from blog import models
from libs.tools import json_success, json_failed


def login(request):
    data = {
        'msg': request.GET.get('msg', '')
    }

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if not user:
            data['msg'] = '账号或密码错误'
        elif not user.is_active:
            data['msg'] = '账号已被禁用，请联系超级管理员解封'
        elif not user.is_superuser:
            data['msg'] = '您没有权限登录管理后台'
        else:
            auth.login(request, user)
            return redirect('/backend')

    return render(request, 'tabler/login.html', data)


def logout(request):
    auth.logout(request)
    return redirect('/backend/login')


def index(request):
    return render(request, 'backend/index.html')


def banner_list(request):
    data = {
        'objs': models.Banner.objects.all(),
        'img_fields': ['img'],
        'choices_fields': [],
        'money_fields': [],
        'banner_active': 'active',
    }

    return render(request, 'backend/base_list.html', data)


def banner_form(request):
    _id = request.GET.get('id')
    model = models.Banner

    form = model.form('privacy')
    obj = model.objects.get(id=_id) if _id else None

    if request.method == 'POST':
        # 价格乘以100入库
        # form_data = request.POST.copy()
        # form_data['price'] = int(float(form_data.get('price', 0) or 0) * 100)
        # form = form(form_data, instance=obj)

        form = form(request.POST, instance=obj)
        if form.is_valid():

            form.save()
            messages.success(request, '修改成功')
            return redirect(request.META['HTTP_REFERER'].replace('form', 'list'))
    else:
        form = form(instance=obj)

    data = {
        'model': model,
        'form': form,
        'img_fields': [],
        'imgs_fields': ['img'],
        'disabled': [],
        'money_fields': [],
        'richtext_fields': ['desc'],
        'banner_active': 'active',
    }

    return render(request, 'backend/base_form.html', data)


def banner_delete(request):
    id = request.GET.get('id', None)
    model = models.Banner

    obj = model.objects.get(id=id)

    obj.delete()

    return redirect(request.META['HTTP_REFERER'].replace('form', 'list'))

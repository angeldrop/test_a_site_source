from django.shortcuts import render,redirect,reverse
from django.core.mail import send_mail
from django.contrib import auth,messages
from accounts.models import Token
import sys

# Create your views here.
def send_login_email(request):
    email=request.POST['email']
    token=Token.objects.create(email=email)
    url=request.build_absolute_uri(
        reverse('login')+'?token='+str(token.uid)
    )
    message_body=f'使用这个链接去登陆系统：\n\n{url}'
    send_mail(
        '你的登录超级表单项目的链接',
        message_body,
        'fffdan111@163.com',
        [email],
    )
    messages.add_message(
        request,
        messages.SUCCESS,
        "Check your email,we've sent you a link you can use to log in."
    )
    return redirect('/')
    
def login(request):
    user=auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')
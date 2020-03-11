from django.shortcuts import render,redirect

# Create your views here.
def send_login_email(request):
    email=request.POST['email']
    send_mail(
        '你的登录超级表单项目的链接',
        '使用这个链接去登陆系统：',
        'fffdan111@163.com',
        [email],
    )

    return redirect('/')
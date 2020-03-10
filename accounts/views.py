from django.shortcuts import redirect,render
import uuid
import sys
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login


from accounts.models import Token
# Create your views here.
def send_login_email(request):
    email=request.POST['email']
    uid=str(uuid.uuid4())
    Token.objects.create(email=email,uid=uid)
    print('saving uid',uid,'for email',emial,file=sys.stderr)
    url=request.build_absolute_uri(f'/accounts/login?uid={uid}')
    send_mail(
        '你的登录超级表单项目的链接',
        f'使用这个链接去登陆系统：\n\n{url}',
        'noreply@superlists',
        [email],
    )
    return render(request,'login_email_sent.html')


def login(request):
    print('login view',file=sys.stderr)
    uid=request.GET.get('uid')
    user=authenticate(uid=uid)
    if user is not None:
        auth_login(request,user)
    return redirect('/')
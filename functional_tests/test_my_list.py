from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY,SESSION_KEY,get_user_model
from django.contrib.sessions.backends.db import SessionStore


from .base import FunctionalTest


User=get_user_model()


class MyListTest(FunctionalTest):

    def create_pre_authenticated_session(self,email):
        user=User.objects.create(email=email)
        session=SessionStore()
        session[SESSION_KEY]=user.pk
        session[BACKEND_SESSION_KEY]=settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        #为了设定cookie，我们需要先访问网站
        #404页面是加载最快的
        self.browser.get(self.live_server_url+"/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/'
        ))
        
        
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email='edith@example.com'
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)
        #迪达拉是已登录用户
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)
        
        
        self.create_pre_authenticated_session('edith@example.com')
    
    
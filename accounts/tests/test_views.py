from django.test import TestCase
from unittest.mock import patch,call
import accounts.views
from accounts.models import Token,User


@patch('accounts.views.auth')
class LoginViewTest(TestCase):
    def test_redirect_to_home_page(self,mock_auth):
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')
    
    
    def test_calls_authenticate_with_uid_from_get_request(self,mock_auth):
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid='abcd123')
        )
    
    
    def test_calls_auth_login_with_user_if_there_is_one(self,mock_auth):
        response=self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request,mock_auth.authenticate.return_value)
        )
    
    
    def test_does_not_login_if_user_is_not_authenticated(self,mock_auth):
        mock_auth.authenticate.return_value=None
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(mock_auth.login.called,False)


class SendLoginEmailViewTest(TestCase):
    
    
    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self,mock_send_mail):
        
        
        self.client.post('/accounts/send_login_email',data={
            'email':'fffdan044@163.com'
        })
        
        
        self.assertEqual(mock_send_mail.called,True)
        (subject,body,from_email,to_list),kwargs=mock_send_mail.call_args
        self.assertEqual(subject,'你的登录超级表单项目的链接')
        self.assertEqual(from_email,'fffdan111@163.com')
        self.assertEqual(to_list,['fffdan044@163.com'])


    def test_adds_success_message(self):
        response=self.client.post('/accounts/send_login_email',data={
            'email':'fffdan044@163.com'
        },follow=True)
        
        message=list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            f"检查你的邮箱，我们已经发送地址到您的邮箱(fffdan044@163.com)了！！"
        )
        
        
    def test_creates_token_associated_with_email(self):
        self.client.post('/accounts/send_login_email',data={
            'email':'fffdan044@163.com'
        })
        
        token=Token.objects.first()
        self.assertEqual(token.email,'fffdan044@163.com')
        
        
    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self,mock_send_mail):
        self.client.post('/accounts/send_login_email',data={
            'email':'fffdan044@163.com'
        })
        
        token=Token.objects.first()
        expected_url=f'http://testserver/accounts/login?token={token.uid}'
        (subject,body,from_email,to_list),kwargs=mock_send_mail.call_args
        self.assertIn(expected_url,body)
        
        

class LoginViewTest(TestCase):
    def test_redirect_to_home_page(self):
        response=self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response,'/')
        

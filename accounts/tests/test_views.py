from django.test import TestCase
import accounts.views


class SendLoginEmailViewTest(TestCase):
    def test_redirect_to_home_page(self):
        response=self.client.post('/accounts/send_login_email',data={
            'email':'fffdan044@163.com'
        })
        self.assertRedirects(response,'/')
    
    
    def test_sends_mail_to_address_from_post(self):
        self.send_mail_called=False
        
        def fake_send_mail(subject,body,from_email,to_list):
            self.send_mail_called=True
            self.subject=subject
            self.body=body
            self.from_email=from_email
            self.to_list=to_list
            
        accounts.views.send_mail=fake_send_mail
        
        self.client.post('/accounts/send_login_email',data={
            'email':'fffdan044@163.com'
        })
        
        
        self.assertTrue(self.send_mail_called)
        self.assertEqual(self.subject,'你的登录超级表单项目的链接')
        self.assertEqual(self.from_email,'fffdan111@163.com')
        self.assertEqual(self.to_list,['fffdan044@163.com'])
   
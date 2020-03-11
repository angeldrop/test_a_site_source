from django.core import mail
from selenium .webdriver.common.keys import Keys
import re


from .base import FunctionalTest


TEST_EMAIL='fffdan043@163.com'
SUBJECT='你的登录超级表单项目的链接'


class LoginTest(FunctionalTest):

    def test_layout_and_styling(self):
        # 迪达拉登录首页
        # 他注意到导航栏有”登录“区域
        # 看到要求输入电子邮箱，他便输入了
        self.browser.get(self.server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)


        # 出现消息，说邮件已发出
        self.wait_for(lambda:self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))
        
        #他看到邮件并查看之
        email=mail.outbox[0]
        self.assertIn(TEST_EMAIL,email.to)
        self.assertEqual(email.subject,SUBJECT)
        
        #邮件中有个URL链接
        self.assertIn('使用这个链接去登陆系统',email.body)
        url_search=re.search(r'http://.+/.+$',email.body)
        if not url_search:
            self.fail(f'没有发现url地址在消息：\n{email.body}')
        url=url_search.group(0)
        self.assertIn(self.live_server_url,url)
        
        #他点击了链接
        self.browser.get(url)
        #他登录了！！
        self.wait_for(
            lambda:self.browser.find_element_by_link_text('登出')
        )
        navbar=self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL,navbar.text)
        

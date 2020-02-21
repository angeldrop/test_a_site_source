# http://175.24.111.140:8080
from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser=webdriver.Firefox()
        self.browser.implicitly_wait(3)
    def tearDown(self):
        self.browser.quit()
    def test_can_start_a_list_and_retrieve_it_later(self):
        #迪达拉听说了一个很酷的在线待办事项应用
        #他去看了应用首页
        self.browser.get('http://localhost:8000')
        
        #他注意到标题处有“To-Do”这个词
        self.assertIn('To-Do',self.browser.title)
        self.fail('Finish the test!')
        
        #应用邀请他输入一个代办事项
        
if __name__=='__main__':
    unittest.main()    #warnings='ignore'
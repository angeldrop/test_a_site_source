# http://175.24.111.140:8080    Firefox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from time import sleep

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser=webdriver.Firefox()
        self.browser.implicitly_wait(3)
        
    def tearDown(self):
        self.browser.quit()
        
    def check_for_row_in_list_table(self,row_text):
        sleep(1)
        table=self.browser.find_element_by_id('id_list_table')
        rows=table.find_elements_by_tag_name('tr')
        self.assertIn(row_text,[row.text for row in rows])
        
    def test_can_start_a_list_and_retrieve_it_later(self):
        #迪达拉听说了一个很酷的在线待办事项应用
        #他去看了应用首页
        self.browser.get('http://localhost:8000')
        
        #他注意到网页头部和标题处都有“To-Do”这个词
        self.assertIn('To-Do',self.browser.title)
        header_text=self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)
        
        #应用邀请他输入一个代办事项
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                            inputbox.get_attribute('placeholder'),
                            'Enter a to-do item'
        )
        
        #迪达拉在一个文本框中输入了“买了孔雀羽毛”Buy Peacock feathers
        #他的爱好是用羽毛做炸弹
        inputbox.send_keys('Buy Peacock feathers')
        
        #他按回车后，页面更新了
        #待办事项表格中显示了“1： Buy Peacock feathers”
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1:Buy Peacock feathers')
        # self.assertIn('1:Buy Peacock feathers',[row.text for row in rows])
        
        #页面中又显示了一个文本框，可以输入其他代办事项
        #他输入了“Use peacock feaher to make a bomb”
        #迪达拉很有条理和耐心
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feaher to make a bomb')
        inputbox.send_keys(Keys.ENTER)       

        #页面再次更新，他的清单中有了两个项目
        self.check_for_row_in_list_table('1:Buy Peacock feathers')
        self.check_for_row_in_list_table('2:Use peacock feaher to make a bomb')
        #迪达拉想知道这个网站是否会记住他的清单
        #他看到网站为他生成了唯一的URL
        #页面中的一些文字解说这个功能
        self.fail('Finish the test!')
        
        #他访问的那个URL，发现待办事项清单还在

        
if __name__=='__main__':
    unittest.main()    #warnings='ignore'
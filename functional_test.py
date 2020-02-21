# http://175.24.111.140:8080
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
        
        #他注意到网页头部和标题处都有“To-Do”这个词
        self.assertIn('To-Do',self.browser.title)
        header_text=self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)
        
        #应用邀请他输入一个代办事项
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                            inputbox.get_attribute(placeholder),
                            'Enter a to-do item'
        )
        
        #迪达拉在一个文本框中输入了“买了孔雀羽毛”
        #他的爱好是用羽毛做炸弹
        inputbox.send_keys('Buy Peacock feathers')
        
        #他按回车后，页面更新了
        #待办事项表格中显示了“1： Buy Peacock feathers”
        inputbox.send_keys(Keys.ENTER)
        
        table=self.browser.find_element_by_id('id_list_table')
        rows=self.browser.find_elements_by_tag_name('tr')
        self.assertTrue(
                        row.text=='1:Buy Peacock feathers' for row in rows
        )
        
        #页面中又显示了一个文本框，可以输入其他代办事项
        #他输入了“Use peacock feaher to make a bomb”
        #迪达拉很有条理和耐心
        self.fail('Finish the test!')
        
        #页面再次更新，他的清单中有了两个项目
        
        

        
if __name__=='__main__':
    unittest.main()    #warnings='ignore'
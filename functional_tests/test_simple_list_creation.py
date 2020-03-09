# http://175.24.111.140:8080    FirefoxChrome
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep


class NewVisitorTest(FunctionalTest):
        
    def test_can_start_a_list_and_retrieve_it_later(self):
        #迪达拉听说了一个很酷的在线待办事项应用
        #他去看了应用首页
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024,768)
        
        
        #他注意到网页头部和标题处都有“To-Do”这个词
        self.assertIn('To-Do',self.browser.title)
        header_text=self.browser.find_element_by_tag_name('h1').text
        self.assertIn('待办事项清单',header_text)
        
        #应用邀请他输入一个代办事项
        #他看到输入框完美的居中显示
        inputbox=self.get_item_input_box()
        sleep(2)
        # self.assertAlmostEqual(
                                # inputbox.location['x']+inputbox.size['width']/2,
                                # 1024/2,
                                # delta=5
        # )
        self.assertEqual(
                            inputbox.get_attribute('placeholder'),
                            '在此填入待办事项'
        )
        
        #迪达拉在一个文本框中输入了“买了孔雀羽毛”Buy Peacock feathers
        #他的爱好是用羽毛做炸弹
        inputbox.send_keys('Buy Peacock feathers')
        
        #他按回车后，被带到了新URL
        #待办事项表格中显示了“1： Buy Peacock feathers”
        inputbox.send_keys(Keys.ENTER) 
        sleep(0.5)
        didala_list_url=self.browser.current_url
        self.assertRegex(didala_list_url,'/lists/.+')

        self.check_for_row_in_list_table('1:Buy Peacock feathers')
        # self.assertIn('1:Buy Peacock feathers',[row.text for row in rows])
        
        #页面中又显示了一个文本框，可以输入其他代办事项
        #他输入了“Use peacock feaher to make a bomb”
        #迪达拉很有条理和耐心
        inputbox=self.get_item_input_box()
        inputbox.send_keys('Use peacock feaher to make a bomb')
        inputbox.send_keys(Keys.ENTER)   
        

        #页面再次更新，他的清单中有了两个项目
        self.check_for_row_in_list_table('1:Buy Peacock feathers')        
        self.check_for_row_in_list_table('2:Use peacock feaher to make a bomb')
        
        #现在有个叫鸣人的人访问了网站
        
        ##我们使用新浏览器会话
        ##确保鸣人的信息不会从cookie中泄露出来
        self.browser.quit()
        self.browser=webdriver.Firefox()
        self.browser.implicitly_wait(3)
        
        #鸣人访问首页
        #看不到迪达拉的名单
        self.browser.get(self.server_url)
        page_text=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Peacock feathers',page_text)
        self.assertNotIn('make a bomb',page_text)
        
        #鸣人输入待办事项，新建一个清单
        #他不像迪达拉那样热情
        inputbox=self.get_item_input_box()
        inputbox.send_keys('Kagebunnshinn')
        inputbox.send_keys(Keys.ENTER)
        sleep(0.5)
        
        #鸣人想知道这个网站是否会记住他的清单
        #他看到网站为他生成了唯一的URL
        #页面中的一些文字解说这个功能
        naruto_list_url=self.browser.current_url
        self.assertRegex(naruto_list_url,'/lists/.+')
        self.assertNotEqual(naruto_list_url,didala_list_url)
        
        #还是看不到迪达拉的名单
        page_text=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Peacock feathers',page_text)
        self.assertNotIn('make a bomb',page_text)
        
        
        #迪达拉访问的那个URL，发现待办事项清单还在
        self.browser.get(didala_list_url)
        #两人都很满意的去睡觉了


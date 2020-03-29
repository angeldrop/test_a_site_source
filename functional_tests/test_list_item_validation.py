from unittest import skip
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
import time


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    # @skip
    def test_can_not_add_empty_list_items(self):
        #didala访问首页时不小心按了一个空待办事项
        #输入框中没有内容，他就按了回车
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        #浏览器截获了请求
        #清单不会加载
        self.wait_for(lambda:self.browser.find_element_by_css_selector(
        '#id_text:invalid'))
        
        #他输入一些文字后提交，这次好了。
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda:self.browser.find_element_by_css_selector(
        '#id_text:valid'))
        #现在可以提交了
        self.get_item_input_box().send_keys(Keys.ENTER)        
        self.check_for_row_in_list_table('1:Buy milk')
        
        #他比较调皮，有输入一个空项目
        self.get_item_input_box().send_keys(Keys.ENTER)
        
        #又出现了类似的错误提示
        self.check_for_row_in_list_table('1:Buy milk')
        self.wait_for(lambda:self.browser.find_element_by_css_selector(
        '#id_text:invalid'))
        
        
        #输入文字后又没有问题了
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda:self.browser.find_element_by_css_selector(
        '#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1:Buy milk')
        self.check_for_row_in_list_table('2:Make tea')


    def test_cannot_add_duplicate_items(self):
        #didala访问首页，新建一个清单
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1:Buy wellies')
        
        #他不小心输入了一个重复待办事项
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        
        #他看到了一条有帮助的错误消息
        self.check_for_row_in_list_table('1:Buy wellies')
        self.assertEqual(self.get_error_element().text,"表格中已经有相同的待办事项了")


    def test_error_messages_are_cleared_on_input(self):
        #迪达拉新建一个清单，但方法不当，所以出现了一个验证错误
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1:Banter too thick')
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda:self.assertTrue(
            self.get_error_element().is_displayed()
        ))
        
        #为了消除错误，他开始在输入框中输入内容
        time.sleep(1)
        self.get_item_input_box().send_keys('a')
        time.sleep(1)
        #看到错误消息消失了，他很高兴
        self.wait_for(lambda:self.assertFalse(
            self.get_error_element().is_displayed()
        ))
        

        self.fail('write me!!')

from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    # @skip
    def test_can_not_add_empty_list_items(self):
        #didala访问首页时不小心按了一个空待办事项
        #输入框中没有内容，他就按了回车
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')
        
        #首页刷新了，显示一个错误消息
        #提示待办事项不能为空
        error=self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text,"You can't have an empty list item")
        
        #他输入一些文字后提交，这次好了。
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1:Buy milk')
        
        #他比较调皮，有输入一个空项目
        self.browser.find_element_by_id('id_new_item').send_keys('\n')
        
        #又出现了类似的错误提示
        self.check_for_row_in_list_table('1:Buy milk')
        error=self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text,"You can't have an empty list item")
        
        #输入文字后又没有问题了
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea\n')
        self.check_for_row_in_list_table('1:Buy milk')
        self.check_for_row_in_list_table('2:Make tea')









        self.fail('write me!!')

from lists.forms import (
ItemForm,EMPTY_LIST_ERROR,DUPLICATE_ITEM_ERROR,
ExistingListItemForm
)
from lists.models import Item,List
from django.test import TestCase


# Create your tests here.
class ItemFormTest(TestCase):
    def test_form_renders_item_text_input(self):
        form=ItemForm()
        self.assertIn('placeholder="在此填入待办事项"',form.as_p())
        self.assertIn('class="form-control input -lg"',form.as_p())
    
    
    def test_form_validation_for_blank_items(self):
        form=ItemForm(data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_LIST_ERROR]
        )


    def test_form_save_hadles_saving_to_a_list(self):
        list_=List.objects.create()
        form=ItemForm(data={'text':'do me'})
        new_item=form.save(for_list=list_)
        self.assertEqual(new_item,Item.objects.first())
        self.assertEqual(new_item.text,'do me')
        self.assertEqual(new_item.list,list_)


class ExistingListItemFormTest(TestCase):
    def test_form_render_item_text_input(self):
        list_=List.objects.create()
        form=ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="在此填入待办事项"',form.as_p())
    
    
    def test_form_validation_for_blank_items(self):
        list_=List.objects.create()
        form=ExistingListItemForm(for_list=list_,data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'],[EMPTY_LIST_ERROR])
    
    
    def test_form_validation_for_duplicate_items(self):
        list_=List.objects.create()
        Item.objects.create(list=list_,text='no twins!')
        form=ExistingListItemForm(for_list=list_,data={'text':'no twins!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'],[DUPLICATE_ITEM_ERROR])


    def test_form_save(self):
        list_=List.objects.create()
        form=ExistingListItemForm(for_list=list_,data={'text':'hi!'})
        new_item=form.save(for_list=list_)
        self.assertEqual(new_item,Item.objects.all()[0])
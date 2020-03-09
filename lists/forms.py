from django import forms
from lists.models import Item
from django.core.exceptions import ValidationError
EMPTY_LIST_ERROR="不能输入空白的待办事项"
DUPLICATE_ITEM_ERROR="表格中已经有相同的待办事项了"


class ItemForm(forms.models.ModelForm):
    class Meta:
        model=Item
        fields=('text',)
        widgets={
            'text':forms.fields.TextInput(attrs={
                'placeholder':'在此填入待办事项',
                'class':'form-control input -lg',
            }),
        }
        error_messages={
            'text':{'required':EMPTY_LIST_ERROR}
        }
        
        
    def save(self,for_list):
        self.instance.list=for_list
        return super().save()


class ExistingListItemForm(ItemForm):
    def __init__(self,for_list,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.instance.list=for_list
        
        
    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict={'text':[DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)
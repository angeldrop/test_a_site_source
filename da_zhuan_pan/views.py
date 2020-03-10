
from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError
from lists.models import Item,List
from lists.forms import ItemForm,ExistingListItemForm


# Create your views here.
def app_dd(request):
    return render(request,'index.html')
    
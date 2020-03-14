from django.shortcuts import render,redirect


# Create your views here.
def dazhuanpan_homepage(request):
    return render(request,'index.html')
    

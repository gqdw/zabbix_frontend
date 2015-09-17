from django.shortcuts import render
from django.http import HttpResponse
from django import forms

# Create your views here.
class Addbox(forms.Form):
	host = forms.CharField(max_length=30)
	ip = forms.GenericIPAddressField()

def index( request ):
	f = Addbox()
	return render(request ,'index.html',{'form':f})
#	return HttpResponse('ok')

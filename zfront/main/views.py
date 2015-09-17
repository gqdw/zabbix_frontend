from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from api import ZabbixApi

# Create your views here.
class Addbox(forms.Form):
	Z = ZabbixApi('aca','acajingru123P')
	Z.auth()
	Z.getgroup()
	glist =  [] 
	for g in Z.grouplist:
		t = (g.groupid ,g.name)
		glist.append(t)
#	print glist
	GENDER =tuple (glist )
	host = forms.CharField(max_length=30)
	ip = forms.GenericIPAddressField()
	test = forms.ChoiceField(choices = GENDER)

def index( request ):
	f = Addbox()
	return render(request ,'index.html',{'form':f})
#	return HttpResponse('ok')

from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from api import ZabbixApi

# Create your views here.
class Addbox(forms.Form):
	Z = ZabbixApi('aca','acajingru123P')
	Z.auth()
	Z.getgroup()
	Z.gettemplates()
	glist = [] 
	tlist = []
	for g in Z.grouplist:
		t = (g.groupid ,g.name)
		glist.append(t)
#	print glist
	CH_GROUP =tuple (glist )
	for t in Z.templatelist:
		t1 = (t.templateid ,t.name)
		tlist.append(t1)
	CH_TEMPLATE = tuple(tlist)
	host = forms.CharField(max_length=30)
	ip = forms.GenericIPAddressField()
	template = forms.ChoiceField(choices = CH_TEMPLATE)
	group = forms.ChoiceField(choices = CH_GROUP)

def index( request ):
	if request.method == 'POST':
		form = Addbox( request.POST )
		if form.is_valid():
			cd = form.cleaned_data
			print cd['host'],cd['ip'],cd['template'],cd['group']
			return HttpResponse('ok')
	else:
		form = Addbox()
	return render(request ,'index.html',{'form':form})
#	return HttpResponse('ok')

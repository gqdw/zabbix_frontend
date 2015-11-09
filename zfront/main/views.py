from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from api import ZabbixApi
import datetime
import time

# Create your views here.
def getpass():
	with open('.config') as f:
		api_user = f.readline().strip()
		api_pass = f.readline().strip()
	return (api_user,api_pass)

class Addbox(forms.Form):
	(api_user,api_pass) = getpass()
	Z = ZabbixApi(api_user,api_pass)
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
	group = forms.ChoiceField(choices = CH_GROUP)
	template = forms.ChoiceField(choices = CH_TEMPLATE)

def index( request ):
	(api_user,api_pass) = getpass()
	if request.method == 'POST':
		form = Addbox( request.POST )
		if form.is_valid():
			cd = form.cleaned_data
			print cd['host'],cd['ip'],cd['template'],cd['group']
			Z = ZabbixApi(api_user,api_pass)
			Z.auth()
			ret = Z.createhost(cd['host'],cd['ip'],cd['group'],cd['template'])
			print ret
			if ret.has_key('error'):
				isok = 0
			else:
				isfalse = 1
			return  render(request,'index.html',{'form':form,'isok':isok,'isfalse':isfalse})
				#return  render(request,'ok.html',{})
			#return HttpResponse(ret['result'])
	else:
		form = Addbox()
	return render(request ,'index.html',{'form':form})
#	return HttpResponse('ok')

def alerts(request):
	(api_user,api_pass) = getpass()
	Z = ZabbixApi(api_user,api_pass)
	Z.auth()
	d1=datetime.date.today()
	t1=time.mktime(d1.timetuple())
	#Z.getalerts(1443312000)
	Z.getalerts(t1)
	#print len(Z.alerts)
	return render(request,'alerts.html',{'alerts':Z.alerts})





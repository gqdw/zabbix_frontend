

#for zabbix 2.2 
import urllib2
import json
import sys

class Proxy:
	def __init__(self,proxyid,host,status):
		self.proxyid = proxyid
		self.host = host
		self.status = status
	def say(self):
		print '%s %s %s' % (self.proxyid ,self.host ,self.status)

class Group:
	def __init__(self,groupid ,name):
		self.groupid = groupid
		self.name = name
	def say(self):
		print '%s %s' %( self.groupid,self.name)
		


class ZabbixApi:
	def __init__(self,api_user,api_pass):
		self.zabbix_url = "http://zabbix.jiagouyun.com/api_jsonrpc.php"
		self.api_user = api_user
		self.api_pass = api_pass
		self.id = 0
		self.proxylist = []
		self.grouplist = []
	
	def auth(self):
		auth_data={ 'jsonrpc':'2.0','method':'user.login','params':{'user':self.api_user,'password':self.api_pass},'id':0}
		request = urllib2.Request(self.zabbix_url,json.dumps(auth_data))
		request.add_header('Content-Type','application/json')
		response = urllib2.urlopen(request)
		var1 = json.loads(response.read())
		self.auth =  var1['result']
		print self.auth
		self.id += 1

	def getproxy(self):
##json data
		data = {
    "jsonrpc": "2.0",
    "method": "proxy.get",
    "params": {
        "output": "extend",
        "selectInterface": "extend"
    },
    "auth": self.auth,
    "id": self.id}
## end data
		request = urllib2.Request(self.zabbix_url,json.dumps( data ))		
		request.add_header('Content-Type','application/json')
		response = urllib2.urlopen(request)
		var1 = json.loads(response.read())
	#	print var1['result']
		for p in var1['result']:
			theid = p['proxyid']
			thehost = p['host']
			thestatus =  p['status']
			n1 = Proxy( theid,thehost,thestatus )
			self.proxylist.append(n1)
		self.id += 1
	def printproxy(self):
		for i in self.proxylist:
			i.say()
	def getgroup(self):
		data = {
    "jsonrpc": "2.0",
    "method": "hostgroup.get",
    "params": {
        "output": "extend",
    },
    "auth": self.auth,
    "id": self.id }
		request = urllib2.Request(self.zabbix_url,json.dumps( data ))
		request.add_header('Content-Type','application/json')
		response = urllib2.urlopen(request)
		var1 = json.loads(response.read())
		for p in var1['result']:
			groupid = p['groupid']
			name = p['name']
			n1 = Group(groupid,name)
		# for debug
			n1.say()
			self.grouplist.append( n1 )
		self.id += 1
		

if __name__ == '__main__':
	with open('.config') as f:
		api_user = f.readline().strip()
		api_pass = f.readline().strip()
	test = ZabbixApi(api_user,api_pass)
	test.auth()
	test.getproxy()
	test.printproxy()
	test.getgroup()


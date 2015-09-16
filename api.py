

#for zabbix 2.2 
import urllib2
import json
import sys
class ZabbixApi:
	def __init__(self,api_user,api_pass):
		self.zabbix_url = "http://zabbix.jiagouyun.com/api_jsonrpc.php"
		self.api_user = api_user
		self.api_pass = api_pass
		self.id = 0
	
	def auth(self):
		auth_data={ 'jsonrpc':'2.0','method':'user.login','params':{'user':self.api_user,'password':self.api_pass},'id':0}
		request = urllib2.Request(self.zabbix_url,json.dumps(auth_data))
		request.add_header('Content-Type','application/json')
		response = urllib2.urlopen(request)
		var1 = json.loads(response.read())
		self.session =  var1['result']
		print self.session


if __name__ == '__main__':
	with open('.config') as f:
		api_user = f.readline().strip()
		api_pass = f.readline().strip()
	test = ZabbixApi(api_user,api_pass)
	test.auth()



#for zabbix 2.2 
import urllib2
import json
class Template:
	def __init__(self,templateid,name):
		self.templateid = templateid
		self.name = name
	def say(self):
		print '%s %s' %(self.templateid ,self.name)

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
		self.zabbix_url = "http://121.199.41.203/api_jsonrpc.php"
		#self.zabbix_url = "http://zabbix.jiagouyun.com/api_jsonrpc.php"
		self.api_user = api_user
		self.api_pass = api_pass
		self.id = 0
		self.proxylist = []
		self.grouplist = []
		self.templatelist = []
	
	def senddata(self,data):
		request = urllib2.Request(self.zabbix_url,json.dumps(data))
		request.add_header('Content-Type','application/json')
		response = urllib2.urlopen(request)
		return json.loads(response.read())	
		self.id += 1
	
	def auth(self):
		auth_data={ 'jsonrpc':'2.0','method':'user.login','params':{'user':self.api_user,'password':self.api_pass},'id':0}
		ret = self.senddata(auth_data)
		self.auth =  ret['result']
		# for debug
		#print self.auth
	def getalerts(self):
		data = {
		    "jsonrpc": "2.0",
		    "method": "alert.get",
		    "params": {
		        "output": "extend",
		        "actionids": "31"
		    },
		    "auth": self.auth,
		    "id": self.id
		}
		ret = self.senddata(data)
		print ret

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
		ret = self.senddata(data)
	#	print ret['result']
		for p in ret['result']:
			theid = p['proxyid']
			thehost = p['host']
			thestatus =  p['status']
			n1 = Proxy( theid,thehost,thestatus )
			self.proxylist.append(n1)

	def printproxy(self):
		for i in self.proxylist:
			i.say()
#todo 
#port 10050
	def gettemplates(self):
		data = {
    "jsonrpc": "2.0",
    "method": "template.get",
    "params": { "output": "extend" },
    "auth": self.auth,
    "id": self.id
	}
		ret = self.senddata(data)
		for t in ret['result']:
			n1 = Template( t['templateid'] ,t['name'])
		# for debug
			#n1.say()
			self.templatelist.append(n1)
		
	def createhost(self,hostname,hostip,groupid,templateid):
		"""create host by zabbix api
			Args:
				hostname,hostip,groupid, templateid
			Returns:
				the json return by zabbix api
				for error it has error key

				{
				    "jsonrpc": "2.0",
				    "error": {
				        "code": -32602,
				        "message": "Invalid params.",
				        "data": "No groups for host \"Linux server\"."
				    },
				    "id": 3
				}
		"""
		data ={
    "jsonrpc": "2.0",
    "method": "host.create",
    "params": {
        "host": hostname,
        "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": hostip,
                "dns": "",
                "port": "10050"
            }
        ],
        "groups": [
            {
                "groupid": groupid
            }
        ],
        "templates": [
            {
                "templateid": templateid
            }
        ],
        "inventory": {
        }
    },
    "auth": self.auth,
    "id": self.id
	}
		ret = self.senddata(data)
	# for debug
	#	print ret
		return ret
		

	def getgroup(self):
		data = {
    "jsonrpc": "2.0",
    "method": "hostgroup.get",
    "params": {
        "output": "extend",
    },
    "auth": self.auth,
    "id": self.id }
		ret = self.senddata(data)
		for p in ret['result']:
			groupid = p['groupid']
			name = p['name']
			n1 = Group(groupid,name)
		# for debug
		#	n1.say()
			self.grouplist.append( n1 )
		

if __name__ == '__main__':
	with open('.config') as f:
		api_user = f.readline().strip()
		api_pass = f.readline().strip()
	test = ZabbixApi(api_user,api_pass)
	test.auth()
	#def createhost(self,hostname,hostip,groupid,templateid):
	#test.createhost('acatest','10.0.0.126','29', '10429')
#	test.getproxy()
#	test.printproxy()
#	test.getgroup()
#	test.gettemplates()
	test.getalerts()



#for zabbix 2.2 
import urllib2
import json
import datetime
import time
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
		self.id += 1
		return json.loads(response.read())	
	
	def auth(self):
		auth_data={ 'jsonrpc':'2.0','method':'user.login','params':{'user':self.api_user,'password':self.api_pass},'id':0}
		ret = self.senddata(auth_data)
		self.auth =  ret['result']
	#	print auth_data
	#	print ret
		# for debug
		#print self.auth
	def getalerts(self,timestamp):
# for debug
#1443312000	
#		timestamp = '1443312000'
		data = {
		    "jsonrpc": "2.0",
		    "method": "alert.get",
		    "params": {
		        "output": "extend",
				"mediatypeids": "5",
				"time_from":timestamp,
		    },
		    "auth": self.auth,
		    "id": self.id
		}
		ret = self.senddata(data)
###
### {u'eventid': u'1182709', u'mediatypeid': u'5', u'alerttype': u'0', u'alertid': u'112671', u'clock': u'1443417182', u'error': u'', u'userid': u'42', u'retries': u'0', u'status': u'1', u'actionid': u'25', u'sendto': u'15921891876', u'message': u'Trigger: searchcenter 8480\nTrigger status: PROBLEM\n\nItem values:\n\n1. searchcenter  8480 (xml-app05:net.tcp.listen[8480]): 1', u'esc_step': u'1', u'subject': u'\u3010\u9a7b\u4e91\u76d1\u63a7\u4e2d\u5fc3\u3011PROBLEM: searchcenter 8480:xml-app05'}
###
#datetime.fromtimestamp(timestamp)
#		print data
#		print ret
		for p in ret['result']:
			print p['clock'],datetime.datetime.fromtimestamp(float(p['clock'])),p['sendto'],p['subject']

	# for debug
#		print ret

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
	t = datetime.date.today()
	timestamp = time.mktime(t.timetuple())	
# for debug
#	print int(timestamp)
	test.getalerts(int(timestamp))




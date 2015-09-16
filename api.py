import urllib2
import json
import sys
zabbix_url="http://zabbix.jiagouyun.com/api_jsonrpc.php"

api_user = sys.argv[1]
api_pass = sys.argv[2]
	
auth_data={ 'jsonrpc':'2.0','method':'user.login','params':{'user':api_user,'password':api_pass},'id':0}
def get_auth():
	request=urllib2.Request(zabbix_url,json.dumps(auth_data))
	request.add_header('Content-Type','application/json')
	response=urllib2.urlopen(request)
	var1=json.loads(response.read())
	return var1['result']
session=get_auth()
print session



import http.client
#import client
import hashlib
import pprint


def getCurrentWebsiteHash(weburl):
	httpConn = http.client.HTTPSConnection(weburl)
	httpConn.request('GET', weburl)

	resp = httpConn.getresponse()
	data = resp.read()

	hash_object = hashlib.md5( data )
	print(hash_object.hexdigest())

	return hash_object.hexdigest()

def getWebList():
	webRecordList = [ {'website':'www.google.com', 'lasthashcode':'xxx'} ]
	return webRecordList

def checkWebList(weblist):
	for webrecord in weblist:
		pprint.pprint(webrecord)
		currWebHash = getCurrentWebsiteHash( webrecord['website'])
		if currWebHash != webrecord['lasthashcode']:
			print( 'Website ' + webrecord['website'] + ' has changed ')

if __name__ == "__main__":
	weblist = getWebList()
	checkWebList( weblist )

import http.client
import hashlib
import psycopg2
from psycopg2.extras import RealDictCursor
import traceback
import urllib.parse
import pprint
import os

urllib.parse.uses_netloc.append("postgres")
url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
dbConn = psycopg2.connect( database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
dbCur = dbConn.cursor(cursor_factory=RealDictCursor)

def getCurrentWebsiteHash(weburl):
	print("getting url:"+ weburl)
	httpConn = http.client.HTTPSConnection(weburl)  #Create connection object
	httpConn.request('GET', weburl)	#Get the website

	resp = httpConn.getresponse()	
	data = resp.read()				#Get the webdata into a string object

	hash_object = hashlib.md5( data )	#Createa  hash code
	print(hash_object.hexdigest())		#print hash code

	return hash_object.hexdigest()

def getWebList():
	rows = []
	try:
		dbCur.execute("select * from webcheckerdb" )	#Get all records from database
		rows = dbCur.fetchall()
	except:
		print ("error during select: " + str(traceback.format_exc()) )
	return rows

def checkWebList(weblist):
	for webrecord in weblist:	#Loop through each record in database
		pprint.pprint(webrecord)
		currWebHash = getCurrentWebsiteHash( webrecord['website'])	#Get the current websites latest hash code
		if currWebHash != webrecord['lasthashcode']:				
			print( 'Website ' + webrecord['website'] + ' has changed ')
			try:
				#If there is a change, print out the change, but also update the database so that next time
				#the message wont get triggered again
				dbCur.execute("update webcheckerdb set lasthashcode ='" + str(currWebHash) + "' where id = '" + str(webrecord['id']) +"'" )
				dbConn.commit()
				print( 'Website hash updated for next time')
			except:
				print ("error during update: " + str(traceback.format_exc()) )

if __name__ == "__main__":
	weblist = getWebList()
	checkWebList( weblist )

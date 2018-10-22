import os
from flask import Flask, request
import hashlib
import psycopg2
from psycopg2.extras import RealDictCursor
import traceback
import urllib.parse
import pprint 

app = Flask(__name__) #create an instance of the Flask library
urllib.parse.uses_netloc.append("postgres")
url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
dbConn = psycopg2.connect( database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
dbCur = dbConn.cursor(cursor_factory=RealDictCursor)


@app.route('/list') #whenever this webserver is called with <hostname:port>/hello then this section is called
def list(): #The subroutine name that handles the call
	output = 'Check status:'
	rows = []
	try:
		dbCur.execute("select * from webcheckerdb" )	#Get all records from database
		rows = dbCur.fetchall()
		for webrecord in rows:	#Loop through each record in database
			output = output + '<BR> ' + pprint.pformat(webrecord)
	except:
		output = "error during select: " + str(traceback.format_exc())

	return output #Whatever is returned from this subroutine is what is returned to the requester and is shown on the browser page


@app.route('/hello') #whenever this webserver is called with <hostname:port>/hello then this section is called
def hello(): #The subroutine name that handles the call
	output = 'Hello World'
	return output #Whatever is returned from this subroutine is what is returned to the requester and is shown on the browser page

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000)) #The port to be listening to — hence, the URL must be <hostname>:<port>/ inorder to send the request to this program
	app.run(host='0.0.0.0', port=port)  #Start listening

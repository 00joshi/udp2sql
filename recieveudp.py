# Recieve UDP Data and write to SQLite database - soon also serial data

import socket
import datetime
import time
import thread
import Queue
import sqlite3 as lite

# listening IP and Port
UDP_IP = "127.0.0.1"
UDP_PORT = 8888

def sqlog(fldTime, args):
    con = lite.connect('logdata.db')
    with con:
	cur = con.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS tblMessages( id INTEGER PRIMARY KEY AUTOINCREMENT, t TIMESTAMP DEFAULT CURRENT_TIMESTAMP, sensor TEXT, type TEXT, Message REAL)") 
	sql = "INSERT INTO tblMessages (sensor, type, Message) VALUES (?,?,?)"
	cur.execute(sql, args)
	con.commit()
	con.close
    return

def helloworld():
	print "Hello World"
	

def networklisten():
	sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
	sock.bind((UDP_IP, UDP_PORT))
	while True:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		q.put(data)
	pass
	return

# Defining a Queue object
q = Queue.Queue(0)

# try:
thread.start_new_thread(networklisten, ())
# except:
# 	print "Error: unable to start thread"

while 1:
    while q.empty() != 1:
	item = q.get()
	sqlog(str(datetime.datetime.now()), item.split(" "))
	q.task_done()
        pass
    time.sleep(15) 
    pass

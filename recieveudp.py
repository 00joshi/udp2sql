#!/usr/bin/env python
# Recieve UDP Data and write to SQLite database - soon also serial data

import os
import sys
import socket
import serial
import datetime
import time
import thread
import Queue
import sqlite3 as lite

# Pid File erzeugen um den Prozess wieder zu finden
if os.access(os.path.expanduser("~/.lockfile.recieve.lock"), os.F_OK):
        #if the lockfile is already there then check the PID number
        #in the lock file
        pidfile = open(os.path.expanduser("~/.lockfile.recieve.lock"), "r")
        pidfile.seek(0)
        old_pid = pidfile.readline()
        # Now we check the PID from lock file matches to the current
        # process PID
        if os.path.exists("/proc/%s" % old_pid):
                print "You already have an instance of the program running"
                print "It is running as process %s," % old_pid
                sys.exit(1)
        else:
                print "File is there but the program is not running"
                print "Removing lock file for the: %s as it can be there because of the program last time it was run" % old_pid
                os.remove(os.path.expanduser("~/.lockfile.recieve.lock"))
else:
	pidfile = open(os.path.expanduser("~/.lockfile.recieve.lock"), "w")
	pidfile.write("%s" % os.getpid())
	pidfile.close
# listening IP and Port
UDP_IP = "127.0.0.1"
UDP_PORT = 8888

def sqlog(args):
    con = lite.connect('logdata.db')
    with con:
	cur = con.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS tblMessages( id INTEGER PRIMARY KEY AUTOINCREMENT, t TIMESTAMP DEFAULT CURRENT_TIMESTAMP, sensor TEXT, type TEXT, Message REAL)") 
	sql = "INSERT INTO tblMessages (sensor, type, Message) VALUES (?,?,?)"
	cur.execute(sql,args)
	con.commit()
	con.close
    return
	

def networklisten():
	sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
	sock.bind((UDP_IP, UDP_PORT))
	while True:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		q.put(data)
	pass
	return

# listening on serial
def seriallisten():
	ser = serial.Serial('/dev/ttyUSB4',57600,timeout=5)
	ser.open()
	while True:
		try:
			ser.open()
			ser.flush()
			data = ser.readline()
			print(data)
			if len(data) != 0:
				q.put(data)
		except:
			break
		finally:
			if ser.isOpen():
				ser.close()
	pass
	return

# Defining a Queue object
q = Queue.Queue(0)

try:
	thread.start_new_thread(networklisten, ())
	thread.start_new_thread(seriallisten, ())
except:
	print "Error: unable to start thread"

while 1:
    while q.empty() != 1:
	item = q.get()
#	sqlog(str(datetime.datetime.now()), item.split(" "))
	sqlog(item.split(" "))
	q.task_done()
        pass
    time.sleep(15) 
    pass

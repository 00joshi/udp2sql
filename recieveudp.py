# Recieve UDP Data and write to SQLite database - soon also serial data

import socket
import datetime
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

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
	data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	sqlog(str(datetime.datetime.now()), data.split(" "))

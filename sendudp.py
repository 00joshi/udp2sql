#!/usr/bin/env python

# This Testscript sends UDP packages to test the other script
import socket
UDP_IP = "127.0.0.1" # The Destination - for now localhost
UDP_PORT = 8888 #port we are running on
MESSAGE = "TestValue Radiation 9001" #the testdata

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
# We need to bind a port to make sure the packages are always send from the same source port
sock.bind(('0.0.0.0', 12345))
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

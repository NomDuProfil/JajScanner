import socket
import Tkinter as tk
import time
import threading
import sys
from tkMessageBox import *

def connect():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect(("127.0.0.1", 1111))
	except socket.error, exc:
		return "error"
	return s

def getinformation(sock, information):
	sock.send(information)
	result = sock.recv(10000)
	return cutcut(result)

def startscan(sock, proc):
	sock.send(proc)

def cutcut(becut):
	tmp=""
	liste = []
	if "RESULT;" in becut:
		return becut.split(';')[1]
	if "ERROROUTPUT;" in becut:
		showwarning('Error', 'No output options in tools.txt')
		sys.exit(4)
	if ';' in becut:
		for inf in becut:
			if inf != ";":
				tmp = tmp+inf
			else:
				liste.append(tmp)
				tmp = ""
	elif "No scan" in becut:
		liste.append("No scan found...")
	else:
		liste.append("Pas d arguments")
	return liste

class CheckProcessThread(threading.Thread):

    def __init__(self, textbox, listbox):

        thread = threading.Thread(target=self.run, args=())
        self.textbox = textbox
        self.listbox = listbox
        self.sock = connect()
        thread.daemon = True
        thread.start()

    def run(self):
    	savelistdone=[]
    	while True:
    		print "Dans le thread"
    		result = ""
    		listprogress = getinformation(self.sock, "inprogress")
    		for i in listprogress:
    			result = result+i+" "
			print("Result checkprocess -> %s" % result)
			self.textbox.config(state=tk.NORMAL)
			self.textbox.delete('1.0', tk.END)
			self.textbox.insert(tk.END, "\n"+result)
			self.textbox.config(state=tk.DISABLED)
			listdone = getinformation(self.sock, "done")
			if listdone != savelistdone:
				self.listbox.delete(0, tk.END)
				savelistdone = listdone
				if listdone[0] == "No scan":
					self.listbox.insert(tk.END, inf[0])
				else:
					for i in listdone:
						self.listbox.insert(tk.END, i)
			time.sleep(5)
			

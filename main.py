import Tkinter as tk
import ttk
import network
import sys
from tkMessageBox import *

sock = network.connect()

if sock == "error":
	showwarning('Error', 'Impossible de se connecter...')
	sys.exit(0)

def resize(event, param): 
    pixelX=param.winfo_width()
    pixelY=param.winfo_height()
    notebook["width"]=int(round(pixelX)) 
    notebook["height"]=int(round(pixelY))

def resizeresult(event, win, text):
	pixelX=win.winfo_width()-100
	pixelY=win.winfo_height()-100
	text["width"]=int(round(pixelX))
	text["height"]=int(round(pixelY))

def gettoolsargument(event, comboarg, combotool):
	comboarg['values'] = network.getinformation(sock, "arguments;"+combotool.get())
	comboarg.current(0)

def clicstart(box, combotool, comboarg, target):
	print ("COMBOARG -> %s" % comboarg.get())
	if (target.get().isspace()) or (not target.get()):
		showwarning('Error', 'No target')
	else:
		if " = " in comboarg.get():
			network.startscan(sock, "start;"+combotool.get()+";"+comboarg.get().split(' = ')[1]+";"+target.get())
		elif "Pas d arguments" in comboarg.get():
			network.startscan(sock, "start;"+combotool.get()+"; ;"+target.get())
		else:
			network.startscan(sock, "start;"+combotool.get()+";"+comboarg.get()+";"+target.get())

def clicdownload(target):
	sockresult = network.connect()
	result = network.getinformation(sockresult, "download;"+target)
	print("DOWNLOAD RESULT -> %s" % result)
	with open(target+".txt",'wb') as file:
		file.write(result)
	sockresult.close()

def printer(event):
	sockresult = network.connect()
	result = network.getinformation(sockresult, "getresult;"+listscan.get(listscan.curselection()))
	print result
	windowresult = tk.Tk()
	framee = tk.Frame(windowresult)
	framee.pack(side=tk.TOP, padx=5, pady=5)
	download = tk.Button(framee, text ='Download', command = lambda: clicdownload(listscan.get(listscan.curselection())))
	download.pack(side = tk.TOP)
	textbox = tk.Text(framee, height=300, width=300)
	textbox.pack()
	textbox.config(state=tk.NORMAL)
	textbox.insert(tk.END, result)
	textbox.config(state=tk.DISABLED)
	windowresult.geometry("500x500")
	windowresult.wm_title(listscan.get(listscan.curselection()))
	windowresult.mainloop()
	sockresult.close()


window = tk.Tk()

notebook = ttk.Notebook(window, width=500, height=500)
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)

frame3 = tk.Frame(frame1)
frame3.pack(side=tk.TOP, padx=5, pady=5)

frame4 = tk.Frame(frame1)
frame4.pack(side=tk.TOP)

label = tk.Label(frame3, text="Outils")
label.grid(column=1, row = 0)
label = tk.Label(frame3, text="Arguments")
label.grid(column=2, row = 0)
label = tk.Label(frame3, text="Cibles")
label.grid(column=3, row = 0)

value = tk.StringVar()
comtool = ttk.Combobox(frame3, textvariable=value, state='readonly')
comtool.grid(column = 1, row = 1)
comtool['values'] = network.getinformation(sock, "tools")
comtool.current(0)
valuee = tk.StringVar()
comarg = ttk.Combobox(frame3, textvariable=valuee, state='readonly')
comarg.grid(column = 2, row = 1)
comarg['values'] = network.getinformation(sock, "arguments;"+comtool.get())
comarg.current(0)
comtool.bind("<<ComboboxSelected>>", lambda event: gettoolsargument(event, comarg, comtool))

target = tk.Entry(frame3)
target.grid(column = 3, row = 1)

scanprogress = tk.Text(frame4, height=300, width=500)
scanprogress.pack()
scanprogress.config(state=tk.NORMAL)
scanprogress.config(state=tk.DISABLED)

startscan = tk.Button(frame3, text ='Start', command = lambda: clicstart(scanprogress, comtool, comarg, target))
startscan.grid(column = 4, row = 1)

listscan = tk.Listbox(frame2, height=300, width=500)
listscan.pack()
listscan.bind("<Double-Button-1>", printer)

window.geometry("600x500")
window.bind("<Configure>", lambda event: resize(event,window))

window.wm_title("JajScanner")

notebook.add(frame1, text='Scan en cours')
notebook.add(frame2, text='Scan complete')
notebook.pack()

checkthread = network.CheckProcessThread(scanprogress, listscan)

window.mainloop()
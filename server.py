import socket
import threading
import process
import os

SERVER_PORT = 1234

def command(commands, tool):
    if commands=="tools":
        print "TOOLS"
        return gettools()
    if commands=="arguments":
        print "ARGUMENTS"
        return getarguments(tool.split(';')[1])
    if commands=="start":
        print "START"
        newscan = process.ProcessThread(tool.split(';')[1], tool.split(';')[2], tool.split(';')[3])
        newscan.start()
    if commands=="inprogress":
        print "INPROGRESS"
        return getprocess()
    if commands=="done":
        print "DONE"
        return doneprocess()
    if commands=="getresult":
        print "GETRESULT"
        return content_file(tool.split(';')[1])
    if commands=="download":
        print "DOWNLOAD"
        return content_file(tool.split(';')[1])

def content_file(namefile):
    fp = open("./done/"+namefile+".txt")
    return "RESULT;"+fp.read()

def doneprocess():
    result = ""
    for file in os.listdir("./done"):
        if file.endswith(".txt"):
            result = result+file.rstrip(".txt")+";"
    if result == "":
        return "No scan"
    return result

def getprocess():
    result = ""
    try:
        with open("./inprogress/inprogress.txt") as fp:
            for line in fp:
                result = result+line.rstrip('\n')+";"
    except IOError:
        return ""
    if result == "":
        print "No scan found..."
        return "No scan found..."
    return result

def gettools():
    result=""
    outputoption = False
    tools = getinfofromtools("nametool")
    outputarg = getinfofromtools("outputoption")
    if len(tools) != len(outputarg):
        return "ERROROUTPUT;"
    for t in tools:
        result = result+t+";"
    return result

def getarguments(tool):
    result=""
    pattern = False
    try:
        with open("tools.txt") as fp:
            for line in fp:
                if "nametool" in line and pattern:
                    return result
                if pattern and "outputoption" not in line:
                    result = result+line.rstrip('\n')+";"
                if "nametool" in line and not pattern and tool in line:
                    pattern = True
    except IOError:
        sys.exit(0)
    return None

def getinfofromtools(param):
    listsearch = []
    try:
        with open("tools.txt") as fp:
            for line in fp:
                if line.split(" = ", 1)[0] == param:
                    listsearch.append(line.split(" = ", 1)[1].rstrip('\n'))
        return listsearch
    except IOError:
        sys.exit(0)

def getoutputoption(tool):
    pattern = False
    try:
        with open("tools.txt") as fp:
            for line in fp:
                if "nametool = "+tool in line:
                    pattern = True
                if "outputoption = " in line and pattern:
                    return line.split(" = ", 1)[1].rstrip('\n')
        return listsearch
    except IOError:
        sys.exit(0)

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket

    def run(self): 

        while True:
            r = self.clientsocket.recv(2048)
            print r
            if ';' in r:
                getset = command(r.split(';')[0], r)
            else:
                getset = command(r, "")
            print getset
            if getset == None:
                self.clientsocket.send("Noarg")
            else:
                self.clientsocket.send(getset)

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("",SERVER_PORT))

while True:
    tcpsock.listen(10)
    print( "En ecoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()
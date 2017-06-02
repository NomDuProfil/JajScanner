import shlex, subprocess
import threading
import fileinput
import sys
import os

def processfinished(command):
    for line in fileinput.input("./inprogress/inprogress.txt",inplace =1):
        line = line.strip()
        if line != command:
            sys.stdout.write(line+"\n")

def inprogress(command):
	f = open("./inprogress/inprogress.txt",'a')
	f.write(command+"\n")
	f.close()

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

class ProcessThread(threading.Thread):

    def __init__(self, tool, argument, target):

        threading.Thread.__init__(self)
        self.tool = tool
        self.argument = argument
        self.target = target

    def run(self):
        if "/" in self.target:
            namefile = self.target.replace("/", "")+".txt"
        else:
            namefile = self.target+".txt"
        command = self.tool+" "+self.target+" "+self.argument+" "+getoutputoption(self.tool)+" ./inprogress/"+namefile
        print ("COMMAND -> %s" % command)
        args = shlex.split(command)
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        inprogress(command)
        process.wait()
        processfinished(command)
        os.rename("./inprogress/"+namefile, "./done/"+namefile)
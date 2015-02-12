import subprocess, sys, os, os.path, shutil, collections, pickle, string, datetime, time, fnmatch
from collections import defaultdict
from datetime import datetime as dt
from datetime import date

import subprocess, sys, os, os.path, shutil, ntpath, re
from SimpleXMLRPCServer import SimpleXMLRPCServer as Server
srv = Server(("127.0.0.1", 1337),allow_none=True) # as an example on the same machine
if not srv: exit(1)
#

setAutoWaitTimeout(1200)
# Major rework on 20111128
#
# Define STATIC variables
#
# Major rework 20121022 - Functions, CPU watch and loaddict
# Major rework 20121105 - Exceptions, load dict from os.listdir for real caps
fileloaderror = "ZlAstronomyl.png"
#wait1("JBufferingan.png")
#wait2("1355554016019.png")

CMD = "top -b -n 10 | gawk '/AutoStakkert/ {print $9}'"
test = True
cpuMax = 10

def AS2CPU():
    while True:
    	RegistaxCPU = os.popen(CMD).readlines()
    	cpu = float(RegistaxCPU[0])
    	if test: print cpu
    	if cpu < cpuMax : break
    	sleep(5)
    	print(RegistaxCPU)


def AS2(DATE, TIME):
    switchApp(TIME)
    dragDrop(Pattern("1374182480082.png").targetOffset(-92,-205), "1374182508440.png")
    sleep(2)
    type("a",KEY_CTRL)
    switchApp("AutoStakkert")
    sleep(2)
    dragDrop("1374107314220.png", Pattern("1Qpen.png").similar(0.50)) # SINGLE & RGB?
    sleep(10)
    App.close(TIME)
    switchApp("AutoStakkert")
    sleep(0.5)
    click(Pattern("WidthHeightS.png").targetOffset(20,-91))
    sleep(2)
    click(Pattern("WidthHeightS.png").targetOffset(-9,180))
    sleep(2)
    click(Pattern("AdvancedSett.png").similar(0.61).targetOffset(-17,-22))
    sleep(2)
    click(Pattern("AdvancedSett.png").similar(0.48).targetOffset(-8,52))
#    AS2CPU()
    wait(Pattern("1355554016019.png").similar(0.77))
#    AS2CPU()
    wait(Pattern("1355554016019.png").similar(0.77))
#    AS2CPU()
#Read most recent DATE and times within

popup('I am here')

srv.register_function(AS2)
srv.serve_forever()

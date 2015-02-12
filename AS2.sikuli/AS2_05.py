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


def AS2(FOLDER):
    switchApp("AutoStakkert")
    click(Pattern("1Qpen.png").similar(0.50)) # SINGLE & RGB?
    sleep(1)
    type("n",KEY_ALT)
    sleep(0.5)
    paste(FOLDER)
    sleep(0.5)
    type(Key.ENTER)
    sleep(0.5)
    #click(Pattern("1374247851439.png").similar(0.43))
    click(Pattern("1389797569446.png").similar(0.28).targetOffset(387,128))
    
    sleep(0.5)
    type("a",KEY_CTRL)
    sleep(0.5)
    type(Key.ENTER)
    sleep(2)
    dragDrop(Pattern("1378900299511.png").targetOffset(-179,-6),Pattern("1378900299511.png").targetOffset(-43,-5))
    sleep(2)
    click(Pattern("WidthHeightS.png").similar(0.80).targetOffset(20,-91))
    sleep(0.5)
    click(Pattern("WidthHeightS.png").similar(0.83).targetOffset(-9,180))
    sleep(0.5)
    click(Pattern("AdvancedSett.png").similar(0.59).targetOffset(-17,-22))
    sleep(0.5)
    click(Pattern("AdvancedSett.png").similar(0.48).targetOffset(-8,52))
    sleep(10)
    wait(Pattern("1355554016019.png").similar(0.77))
#    AS2CPU()
    wait(Pattern("1355554016019.png").similar(0.77))
    if exists:(click(Pattern("1395884074220.png").similar(0.36).targetOffset(301,-262)))
#    AS2CPU()
#Read most recent DATE and times within

#popup('I am here')

srv.register_function(AS2)
srv.serve_forever()

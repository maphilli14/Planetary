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
# 20140501 Begin passing custom MP v Single and Drizzle selctions from menus
#
fileloaderror = "ZlAstronomyl.png"
percent='66'


def AS2(FOLDER,AP,Drizzle):
    switchApp("AutoStakkert")
    click(Pattern("1Qpen.png").similar(0.50)) # SINGLE & RGB?
    sleep(1)
    type("n",KEY_ALT)
    sleep(0.5)
    paste(FOLDER)
    sleep(0.5)
    type(Key.ENTER)
    sleep(0.5)
    click(exists(Pattern("1389797569446.png").similar(0.28).targetOffset(387,128),2))
    click(exists("1415665075411.png",2))
    
    
    sleep(0.5)
    type("a",KEY_CTRL)
    sleep(0.5)
    type(Key.ENTER)
    sleep(2)
    dragDrop(Pattern("1378900299511.png").targetOffset(-179,-6),Pattern("1378900299511.png").targetOffset(-43,-5))
    sleep(2)
    #Selection of MP v Single
    print('AP = '+str(AP))
    if AP == 's':
        print('Using Single AP method')
        click(Pattern("WidthHeightS.png").similar(0.69).targetOffset(-54,-137))
        click(Pattern("1415665268913.png").targetOffset(-52,28))
        type('0'+Key.TAB+'0'+Key.TAB+'0'+Key.TAB+str(percent))
        click(Pattern("1415665268913.png").targetOffset(-53,-13))
        type('0'+Key.TAB+'0'+Key.TAB+'0'+Key.TAB+'0')
    else:
        pass
    if AP == 'm':
        print('Using Multi AP method')
        click(Pattern("WidthHeightS.png").similar(0.69).targetOffset(-53,-118))
        click(Pattern("1398957372328.png").targetOffset(-7,160))
        print('Looking for percent')
        click(Pattern("1427196763553.png").targetOffset(54,45))
        type(Key.BACKSPACE)
        sleep(0.1)
        type(str(percent))
        sleep(0.1)
    else:
        pass
    sleep(0.5)
    #Selection of Drizzle Options
    if Drizzle == '1':
        click(Pattern("AdvancedSett.png").similar(0.29).targetOffset(-18,-22))
    elif Drizzle == '3':
        click(Pattern("AdvancedSett.png").similar(0.28).targetOffset(-16,-5))
    else:
        click(Pattern("AdvancedSett.png").similar(0.29).targetOffset(-17,-22))
    sleep(0.5)
    click(Pattern("AdvancedSett.png").similar(0.48).targetOffset(-8,52))
    sleep(10)
    print('')
    print('Waiting for AS2 to complete')
    print('')
    wait(Pattern("1355554016019.png").similar(0.77))
    print('')
    print('Checking for completion again')
    print('')
    wait(Pattern("1355554016019.png").similar(0.77))
    if exists:(click(Pattern("1395884074220.png").similar(0.36).targetOffset(301,-262)))
    sleep(5)
#    AS2CPU()
#Read most recent DATE and times within

#popup('I am here')

srv.register_function(AS2)
srv.serve_forever()

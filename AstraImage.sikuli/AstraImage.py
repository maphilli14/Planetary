from sikuli.Sikuli import *
#
import subprocess, sys, os, os.path, shutil, ntpath, re
from SimpleXMLRPCServer import SimpleXMLRPCServer as Server
srv = Server(("127.0.0.1", 1337),allow_none=True) # as an example on the same machine
if not srv: exit(1)
#
setAutoWaitTimeout(300)
'''
    20150130
    Moved to git and removed locally significat versioning
  
    This script is run after AS2StackWalk.py
    Recreated for Pro on 20120509
     Updated to chunk into defs

	20120928
	Started from scratch re-writing Astro caps
	This file loads previously saved pickle cap data

        20121014
    Adding full raw and sharp support, save as new

    Major rework 20121105 - Exceptions, load dict from os.listdir for real caps

    Updated 20130620 - Added os.list dir instead of dict and new defs to pull out time from file

    Reworked 20130709 to use XML RPC and only leave custom Def's behind, rest is done via python calls

Updated pathing for NewDocDirs2 20130418
'''

import subprocess, sys, os, os.path, shutil, collections, fnmatch, re
from collections import defaultdict

print '\nSikuli script started!\n'
#Vars:

Stacked='D:\\B-Sorted\\Astronomy\\Planetary\\20-Stacked\\'
sharped = Stacked # Location specified by AS2StackWalk.py

#data to work with, in simple terms, the captured data
Ver = 'v10'
RGBd = 'D:\\B-Sorted\\Astronomy\\Planetary\\30-Sharped+RGB\\'
AS2ed = "AS2ed"
FileSyntax = '10m7515'



def sharpeningsetup(Duration,PSF,Iter):
    'Primes the decon settings to taste - per Google Drive Sharpening Settings File'
    print '\n[Sikuli] Setting up sharpening settings\n'
    #
    # Set Variables for each channel
    # Red is typically the highest and the rest will 'down' from there
    #
    # Each is a delta up or down from previous default/channel
    #
    #Existing is 1.0/10 -> Mars G = 1.2/16
    #RPSF = 2
    #RITER = 6
    switchApp("Astra")
    sleep(0.2)
    type("l",KEY_CTRL)
    sleep(0.2)
    click(Pattern("PointSpreadF.png").similar(0.57).targetOffset(-368,-137))
    sleep(0.2)
    click(Pattern("PointSpreadF.png").similar(0.57).targetOffset(-135,-9))
    sleep(0.2)
    #Initial Settings are 1/10, changes for Red to 1.2 and 18
    if PSF >=1:
        for n in range(PSF):
        	type(Key.UP)
        type(Key.TAB)
    elif PSF < 1:
        for n in range(PSF):
        	type(Key.DOWN)
        type(Key.TAB)
    if Iter >=1:
        for n in range(Iter):
        	type(Key.UP)
    if Iter < 1:
        for n in range(Iter):
        	type(Key.DOWN)
    sleep(1)
    dragDrop(Pattern("1395682627883.png").targetOffset(141,35), Pattern("1395682632171.png").targetOffset(-263,-211))
    
    if exists(Pattern("1395682602331.png").targetOffset(339,62),2):click(getLastMatch())
    n=1
    Timer=Duration
    for n in range(Timer):
        print 'Waiting for '+str(n)+' of '+str(Timer)+' sec'
        n=n+1
        sleep(1)
    click(Pattern("1395682632171.png").targetOffset(256,176))
    waitVanish("1395682602331.png")

def prime(DATE, TIME):
    print '\n[Sikuli] Loading initial files to get AstraImage in order\n'
    sharpfldr = os.path.join(sharped, DATE, TIME, 'v10\\')
    firstfile=os.path.join(sharpfldr+os.listdir(sharpfldr)[1])
    switchApp("Astra")
    click("1373393362342.png")
    switchApp("Astra")
    click("1373393362342.png")
    type("f",KEY_ALT)
    sleep(0.5)
    type("o")
    sleep(0.5)
    type("n",KEY_ALT)
    sleep(0.75)
    type(Key.DELETE)
    sleep(0.75)
    print('\nSikuli is loading file '+str(firstfile)+'\n')
    paste(str(firstfile))
    sleep(0.75)
    type(Key.ENTER)



def sharp(ToBeSharped, DATE, TIME,AISettingsVer):
    'Relies on having the proper folders setup for relative pathing from prime Def.  Fed files from ColorMatch Def'
    print '\n[Sikuli] Starting to sharpen your files...\n'
    switchApp("Astra")
    sleep(0.5)
    type("f",KEY_ALT)
    sleep(0.5)
    type("o")
    sleep(0.5)
    type("n",KEY_ALT)
    sleep(0.75)
    type(Key.DELETE)
    sleep(0.75)
    paste(str(ToBeSharped))
    sleep(0.75)
    type(Key.ENTER)
    sleep(0.75)
    if exists((Pattern("1401392122846.png").similar(0.81).targetOffset(-4,38)),2):
        print '\n\nSikuli found a file load error!\n\n'
        click(getLastMatch())
        exit()
    else:
        pass
    switchApp("Astra")
    sleep(0.75)
    type("l",KEY_CTRL)
    sleep(0.5)
    #type(Key.ENTER)
    click(Pattern("PointSpreadF.png").similar(0.57).targetOffset(266,181))
    waitVanish("PointSpreadF-3.png")
    sleep(0.75)
    switchApp("Astra")
    sleep(0.5)
    type("s",KEY_CTRL)
    sleep(0.5)
    paste('Ver-'+AISettingsVer+'-'+ToBeSharped)
    sleep(0.5)
    type("\n")
    if exists(Pattern("1423956186162.png").similar(0.42).targetOffset(80,32),2):
        click(getLastMatch())

    if exists(Pattern("1394391875003.png").similar(0.56).targetOffset(-3,88),2):
            click(getLastMatch())
            waitVanish(Pattern("1394391875003.png").similar(0.56).targetOffset(-3,88))


def RGB(RED,GREEN,BLUE,RGB,DATE, TIME,Duration):
    print '\n[Sikuli] is using AstraImage to combine channels to RGB color image\n'
    sleep(1)
    for n in range(1):
        switchApp("Astra")
        sleep(1)
        type("p",KEY_ALT)
        sleep(0.5)
        type("o")
        sleep(0.2)
        type(Key.TAB + " ")
        sleep(0.75)
        sharpfldr = os.path.join(sharped, DATE, TIME, 'v10')
        paste(sharpfldr)
        sleep(0.5)
        type(Key.ENTER)
        sleep(0.5)
        type("n",KEY_ALT)
        sleep(0.75)
        paste(RED)
        sleep(0.75)
        type(Key.ENTER)
        sleep(0.75)
        type(Key.TAB + Key.TAB + Key.TAB + Key.TAB + Key.TAB + " ")
        type("n",KEY_ALT)
        sleep(0.75)
        paste(GREEN)
        sleep(0.75)
        type(Key.ENTER)
        sleep(0.75)
        type(Key.TAB + Key.TAB + Key.TAB + Key.TAB + Key.TAB + " ")
        type("n",KEY_ALT)
        sleep(0.75)
        paste(BLUE)
        sleep(0.75)
        type(Key.ENTER)
        sleep(0.75)
        type(Key.TAB + Key.TAB + Key.TAB + Key.TAB + Key.TAB + Key.TAB + Key.DOWN + " ")
        sleep(0.2)
        for n in range(17):
            type(Key.TAB)
        click(Pattern("1394806810279.png").targetOffset(29,194))       
        switchApp("Astra")
        n=1
        Timer=Duration
        for n in range(Timer):
            print 'Waiting for '+str(n)+' of '+str(Timer)+' sec'
            n=n+1
            sleep(1)
        sleep(10.0)
        click(Pattern("1394501688302.png").similar(0.42).targetOffset(232,257))
        sleep(2)
        type("s",KEY_CTRL)
        type("n",KEY_ALT)
        sleep(0.75)
        paste(RGB)
        sleep(0.75)
        type(Key.ENTER)
        sleep(2)
        type("y",KEY_ALT)
        sleep(1)
        type(Key.ENTER)
        sleep(1)
        type(Key.ENTER)
        sleep(1)
        type(Key.ENTER)


def TimeMatch(st):
	match=re.search(r'[0-9]+\.[0-9]', st)
	if match:
		result = match.group()
		print result
		return result
	else:
		print "Not Found"

def Counter(TIME,count,QueuedTimes):
    print
    print "__________________________________________________________________________________"
    print "Time is "+TIME+" ("+str(count)+" of "+str(len(QueuedTimes))+")"
    print "__________________________________________________________________________________"
    print


def closeAI():
    print '\nSikuli is closing AstraImage\n'
    sleep(2)
    switchApp("Astra")
    sleep(2)
    switchApp("Astra")
    sleep(2)
    click("1373393362342.png")
    type("f",KEY_ALT)
    sleep(0.5)
    type("x")
    sleep(0.5)    


#
#File Dictionaries
#
fileloaderror = Pattern("ZiAstronomyi.png").similar(0.36)
fileloaderrorB = Pattern("ZlAstronomyl.png").similar(0.64)

srv.register_function(sharpeningsetup)
srv.register_function(prime)
srv.register_function(sharp)
srv.register_function(RGB)
srv.register_function(TimeMatch)
srv.register_function(Counter)
srv.register_function(closeAI)
srv.serve_forever()

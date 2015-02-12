#
import subprocess, sys, os, os.path, shutil, ntpath, re, time
'''
20140518 - Started to break AI scripts into modules
'''
import subprocess, sys, os, os.path, shutil, collections, fnmatch, re, xmlrpclib, logging, distutils.dir_util,AIlib,AISettings
from decimal import *
from collections import defaultdict



def ColorMatch(st):
	for c in COLORS:
		match=re.search(r'^Drizzle15_\w+-\w+-\w+-\w+.\w+-MAP-'+c+'+\w+.tif', st)
		if match:
			result = match.group()
			print c+' file is: ', st
			globals()[c] = st
		else:
			pass

def convColorMatch(st):
	for c in COLORS:
		result=re.match('^conv_\w+-\w+-\w+-\w+.\w+-MAP-'+c+'+\w+.tif',st)
		if result:
			print c+' file is: ', st
			globals()[c] = st
		else:
			pass



def monocopier():
        try:
                print 'copying sharped mono: R = '+IsStackFile[0] 
                shutil.copy2(os.path.join(Stacked, DATE, TIME,Ver,'Ver-'+AISettingsVer+'-'+IsStackFile[0]),os.path.join(RGBd,DATE,'all','Ver'+AISettingsVer,'R',TIME+'.tiff'))
        except:
                e = sys.exc_info()
                print e
        try:
                print 'copying sharped mono: G = '+IsStackFile[1] 
                shutil.copy2(os.path.join(Stacked, DATE, TIME,Ver,'Ver-'+AISettingsVer+'-'+IsStackFile[1]),os.path.join(RGBd,DATE,'all','Ver'+AISettingsVer,'G',TIME+'.tiff'))
        except:
                e = sys.exc_info()
                print e
        try:
                print 'copying sharped mono: B = '+IsStackFile[2]
                shutil.copy2(os.path.join(Stacked, DATE, TIME,Ver,'Ver-'+AISettingsVer+'-'+IsStackFile[2]),os.path.join(RGBd,DATE,'all','Ver'+AISettingsVer,'B',TIME+'.tiff'))
        except:
                e = sys.exc_info()
                print e

        try:
                print 'copying sharped mono: IR = '+IsStackFile[3]
                shutil.copy2(os.path.join(Stacked, DATE, TIME,Ver,'Ver-'+AISettingsVer+'-'+IsStackFile[3]),os.path.join(RGBd,DATE,'all','Ver'+AISettingsVer,'IR',TIME+'.tiff'))
        except:
                e = sys.exc_info()
                print e


def sharpmover(InF,OutD):
    #Move dones to 2.3-Sharped+RGB
    print "Searching for "+OutD+" processed captures"
    print "_____________________________"
    path = os.path.join(Stacked, DATE, TIME, Ver)
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == InF:
                print 'Found ' + file + ' in ' + TIME
                try:
                    shutil.copy2(os.path.join(Stacked,DATE,TIME,Ver,file), os.path.join(RGBd,DATE,"all",OutD,TIME+'.tiff'))
                except:
                        e = sys.exc_info()
                        print e
            else:
                pass

def StackedCleaner():
        print 'Running StackCleaner'
        for TIME in QueuedTimes:
                print TIME
                try:
                        if len(os.listdir(os.path.join(Stacked, DATE, TIME,Ver)))==0:
                                print TIME+' is empty'
                                shutil.rmtree(os.path.join(Stacked, DATE, TIME))
                        else:
                                print TIME+' contains files'
                                distutils.dir_util.copy_tree(os.path.join(Stacked, DATE, TIME), os.path.join(RGBd, DATE, AS2ed,TIME))
                                shutil.rmtree(os.path.join(Stacked, DATE, TIME))
                except:
                        print TIME+' didn\'t get checked'
                        e = sys.exc_info()
                        print e
 
                                


#Settings per https://docs.google.com/document/d/1xuYUnM9cEhxZGYKNxi3pYOVZeqbjEqf5WFF4fr93cek/edit#
#
cr="\n"
#
# === PASS Sharps settings to Sikuli ===
#
PSF=1
Iter=6
#
j1 = 'Best Jupiter settings: \'P\''+cr
j2 = ' PSF=1.1 Iter=16'
j3 = 'Smaller Jupiter settings: \'Q\''+cr
j4 = ' PSF=1.2 Iter=15'+cr+cr
##
m1 = 'Best Mars 1.5x settings: \'G\''+cr
m2 = ' PSF=1.2 Iter=16'+cr
m3 = 'Best Mars 3x settings: \'I\''+cr
m4 = ' PSF=1.6 Iter=18'+cr+cr+cr
#
o1 = 'Pick your current AstraImage version'+cr
o2 = ' Otherwise things will be tagged as XX'+cr
#
#
def menu():
        #this def takes into account the starting values AI uses as 1.0 and 10
        global output,AISettingsVer,PSF,Iter
        output = j1+j2+j3+j4+m1+m2+m3+m4+o1+o2
        AISettingsVer=raw_input(output)
        print cr
        strPSF=float(raw_input("PSF= "))
        strIter=int(raw_input("Iter= "))

        if re.match('[A-Za-z]',AISettingsVer):
            print "User Picked"
            print AISettingsVer
        else:
            print "you didn't pick, using XX as No Choice"
            AISettingsVer='XX'
        print 'Your PSF = %s, with %s Iterations' %(strPSF,strIter)
        PSF=int((strPSF-1)*10)
        Iter=int(strIter-10)


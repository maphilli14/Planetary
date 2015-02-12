#
import subprocess, sys, os, os.path, shutil, ntpath, re, time
'''
20140518 - Started to break AI scripts into modules
'''
import subprocess, sys, os, os.path, shutil, collections, fnmatch, re, xmlrpclib, logging, distutils.dir_util,AISettings
from decimal import *
from collections import defaultdict
from AstraImage import main

def planetgrabber():
	global Planet
	global Planetstr	
	Planet=raw_input('\n\nWhich Planet? Enter a single letter\nfor Mars, Jupiter or Saturn [m,j,s]:')
	Planetdict={'m':'Mars','j':'Jupiter','s':'Saturn'}
	if Planet=='m':
		Planetstr='Mars'
	elif Planet=='s':
		Planetstr='Saturn'
	elif Planet=='j':
		Planetstr='Jupiter'

	print '\n\n you selected\n '+str(Planetstr)

def menu1():
	planetgrabber()
	global Planetstr, AISettingsVer
	conf=raw_input('\n\n\nThis script will stack your images in AstraImage\n Configure options? (y/n) ')
	if conf == 'y':
		print 'Ok, let\'s customize this...\n'
		menu2()
	else:
		if Planet=='m':
			Planetstr='Mars'
			AISettingsVer='VerG'
		elif Planet=='s':
			Planetstr='Saturn'
			AISettingsVer='VerN'
		elif Planet=='j':
			Planetstr='Jupiter'
			AISettingsVer='VerP'
		settingsloader(AISettingsVer)
	main(PSF,Iter,AISettingsVer)


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
j2 = ' PSF=1.1 Iter=16'+cr
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


def menu2():
        #this def takes into account the starting values AI uses as 1.0 and 10
        global output,AISettingsVer,PSF,Iter,Planetstr
        #output = j1+j2+j3+j4+m1+m2+m3+m4+o1+o2
        print 'Here\'s your settings for '+Planetstr
        print
        if Planetstr=='Mars':
                for k,v in AISettings.Mars.iteritems():
                        print k
                        print v
        if Planetstr=='Jupiter':
                for k,v in AISettings.Jupiter.iteritems():
                        print k
                        print v
        if Planetstr=='Saturn':
                for k,v in AISettings.Saturn.iteritems():
                        print k
                        print v
        output = o1+o2
        AISettingsVer=raw_input(output)
        print cr
        if Planetstr=='Mars':
        	sPSF=str(AISettings.Mars["Ver"+AISettingsVer][0])
        	sIter=str(AISettings.Mars["Ver"+AISettingsVer][1])
        if Planetstr=='Jupiter':
        	sPSF=str(AISettings.Jupiter["Ver"+AISettingsVer][0])
        	sIter=str(AISettings.Jupiter["Ver"+AISettingsVer][1])
        if Planetstr=='Saturn':
        	sPSF=str(AISettings.Saturn["Ver"+AISettingsVer][0])
        	sIter=str(AISettings.Saturn["Ver"+AISettingsVer][1])
        if re.match('[A-Za-z]',AISettingsVer):
            print "User Picked"
            print AISettingsVer
        else:
            print "you didn't pick, using XX as No Choice"
            AISettingsVer='XX'
        print 'Your PSF = %s, with %s Iterations' %(sPSF,sIter)
        valuesanitizer(sPSF,sIter)
        print 'Let\'s start sharpening!'
        main(PSF,Iter,AISettingsVer)
        


def settingsloader(Ver):
	global Planet,PSF,Iter
	if Planet=='m':
		Planetstr='Mars'
		print 'Default settings for '+Planetstr+' are:\n'+str(AISettings.Mars[Ver])
		sPSF=str(AISettings.Mars[Ver][0])
		sIter=str(AISettings.Mars[Ver][1])
	elif Planet=='s':
		Planetstr='Saturn'
		print 'Default settings for '+Planetstr+' are:\n'+str(AISettings.Saturn[Ver])
		sPSF=AISettings.Saturn[Ver][0]
		sIter=AISettings.Saturn[Ver][1]
	elif Planet=='j':
		Planetstr='Jupiter'
		print 'Default settings for '+Planetstr+' are:\n'+str(AISettings.Jupiter[Ver])
		sPSF=AISettings.Jupiter[Ver][0]
		sIter=AISettings.Jupiter[Ver][1]
	valuesanitizer(sPSF,sIter)

def valuesanitizer(P,I):
        global PSF,Iter
        getcontext().prec = 1
        rPSF=float(Decimal(P))
        if rPSF < 2:
                PSF=int((Decimal(rPSF)-1)*10)
        else:
                getcontext().prec = 2
                PSF=int((rPSF-1)*10)
        Iter=int(float(I)-10)
        return PSF,Iter

                                

menu1()

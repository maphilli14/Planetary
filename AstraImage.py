#
import subprocess, sys, os, os.path, shutil, ntpath, re, time
'''
This 

'''

import subprocess, sys, os, os.path, shutil, collections, fnmatch, re, xmlrpclib, logging, distutils.dir_util,AIlib
from decimal import *
from collections import defaultdict

#Editable vars
Sikuli='D:\\D-Permanent\\Software\\Win7Installs\\Sikuli\\runIDE.cmd'
Sikuliarg1='-r'
scriptname='D:\\D-Permanent\\Scripts\\Git\\Planetary\\AstraImage.sikuli'
Duration=12
COLORS=['R', 'G', 'B', 'IR']
Ver = 'v10'
AS2ed = "AS2ed"
AIpath='D:\D-Permanent\Software\Win7Installs\Astra Image 3.0 Pro'
Stacked='D:\\B-Sorted\\Astronomy\\Planetary\\20-Stacked\\'
RRegex='^Drizzle15_.*-R.*'
GRegex='^Drizzle15_.*-G.*'
BRegex='^Drizzle15_.*-B.*'
IRRegex='^Drizzle15_.*-IR.*'


def DATETIME():
     global DATE,DATES,TIMES,TIME,QueuedTimes
     #Read most recent DATE and times within
     DATES = os.listdir(Stacked)
     DATE = sorted(DATES)[-1]
     TIMES=[]
     for d in os.listdir(os.path.join(Stacked,DATE)):
          if 'v10' in os.listdir(os.path.join(Stacked,DATE,d)):
               TIMES.append(d)
     print 'Running StackCleaner'
     for TIME in [TIME for TIME in TIMES if 'v10' in os.listdir(os.path.join(Stacked, DATE, TIME))]:
           print TIME
           try:
                   if len(os.listdir(os.path.join(Stacked, DATE, TIME,Ver)))==0:
                           print TIME+' is empty'
                           shutil.rmtree(os.path.join(Stacked, DATE, TIME))
                   else:
                           print TIME+' contains files'
                           pass
                           #distutils.dir_util.copy_tree(os.path.join(Stacked, DATE, TIME), os.path.join(RGBd, DATE, AS2ed,TIME))
                           #shutil.rmtree(os.path.join(Stacked, DATE, TIME))
           except:
                   print TIME+' failed to clean'
                   e = sys.exc_info()
                   print e
     QueuedTimes=[]
     try:
          QueuedTimes=[TIME for TIME in TIMES if 'v10' in os.listdir(os.path.join(Stacked, DATE, TIME))]
     except:
          print TIME+' failed to clean'
          e = sys.exc_info()
          print e


#Static Vars
AISettingsVer=''
#sharped = Stacked # Location specified by AS2StackWalk.py

RGBd = 'D:\\B-Sorted\\Astronomy\\Planetary\\30-Sharped+RGB\\'



#Movers
def monocopier(AISettingsVer,TIME):
     global ColorFiles
     print
     try:
           print 'copying sharped mono: R = '+ColorFiles['R'][1]
           shutil.copy2(os.path.join(Stacked, DATE, TIME,Ver,ColorFiles['R'][1]),os.path.join(RGBd,DATE,'all','Ver'+AISettingsVer,'R',TIME+'.tiff'))
     except:
           e = sys.exc_info()
           print e
     try:
           print 'copying sharped mono: G = '+ColorFiles['G'][1] 
           shutil.copy2(os.path.join(Stacked, DATE, TIME,Ver,ColorFiles['G'][1]),os.path.join(RGBd,DATE,'all','Ver'+AISettingsVer,'G',TIME+'.tiff'))
     except:
           e = sys.exc_info()
           print e
     try:
           print 'copying sharped mono: B = '+ColorFiles['B'][1]
           shutil.copy2(os.path.join(Stacked, DATE, TIME,Ver,ColorFiles['B'][1]),os.path.join(RGBd,DATE,'all','Ver'+AISettingsVer,'B',TIME+'.tiff'))
     except:
           e = sys.exc_info()
           print e

     try:
           print 'copying sharped mono: IR = '+ColorFiles['IR'][1]
           shutil.copy2(os.path.join(Stacked, DATE, TIME,Ver,ColorFiles['IR'][1]),os.path.join(RGBd,DATE,'all','Ver'+AISettingsVer,'IR',TIME+'.tiff'))
     except:
           e = sys.exc_info()
           print e


def sharpmover(InF,OutD,TIME):
    #Move dones to 2.3-Sharped+RGB
    print "\n\nSearching for "+OutD+" processed captures"
    print "_____________________________"
    path = os.path.join(Stacked, DATE, TIME, Ver)
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == InF:
                print 'Found ' + file + ' in ' + TIME
                try:
                    shutil.copy2(os.path.join(Stacked,DATE,TIME,Ver,file), os.path.join(RGBd,DATE,"all",OutD,TIME+'.tiff'))
                except:
                     print '\nFound error in sharpmover:'
                     e = sys.exc_info()
                     print e
            else:
                pass

               


######################################################
#
# RUNTIME
#
######################################################
def main(PSF,Iter,AISettingsVer):
     global COLORS,ColorFiles
     DATETIME()
     AI=subprocess.Popen(os.path.join(AIpath)+'\\ai3pro.exe')
     cli = xmlrpclib.ServerProxy("http://127.0.0.1:1337",allow_none=True)
     proc = subprocess.Popen([Sikuli,Sikuliarg1,scriptname])
     #abs wait for sikuli script to load and be ready for xmlrpc, find better way
     time.sleep(30)
     getcontext().prec = 1
     for C in COLORS:
          try:
               os.makedirs(os.path.join(RGBd,DATE,'all','Ver'+AISettingsVer,C))
          except os.error:
               pass
     print QueuedTimes
     #Counter
     count=1
     #Load initial Image to make AI behave properly
     try:
          STACKEDFILES=os.listdir(os.path.join(Stacked,DATE,TIMES[0],'v10'))
     except:
          STACKEDFILES=[]
          print '\nFound error in STACKEDFILES:'
          e = sys.exc_info()
          print e
     if len(STACKEDFILES)==0:
          print 'no files in, '+TIMES[0]+' skipping, and removing folder'
          DATETIME()
          try:
               shutil.rmtree(os.path.join(Stacked, DATE, TIMES[0]))
               print "DELETING "+os.path.join(Stacked, DATE, TIMES[0])+" to "+os.path.join(RGBd, DATE, AS2ed)
               TIMES.remove(TIMES[0])
          except:
               print "Can NOT Delete "+os.path.join(Stacked, DATE, TIMES[0])+" to "+os.path.join(RGBd, DATE, AS2ed)
               pass
     else:
          print '\nConfirmed this folder has files'
     try:
          print '\nLet\'s load a random file from the 1st capture'
          cli.prime(DATE, TIMES[0])
     except Exception as e:
          if e.message == 'IndexError: list index out of range':
               print 'This was the last capture'
     #Setup your settings for each subsquent useage
     cli.sharpeningsetup(Duration,PSF,Iter)
     #
     # BIG STEP to loop over all times in this DATE
     #
     for TIME in QueuedTimes:
          print "\n\n\nTime is "+TIME+" ("+str(count)+" of "+str(len(QueuedTimes))+")"
          count=count+1
          print "__________________________________________________________________________________"
          print
          try:
               STACKEDFILES=os.listdir(os.path.join(Stacked,DATE,TIME,'v10'))
          except:
               print 'This directory is EMPTY, please fix via pre checks like in AS2'
               pass
          RGBSharp='Ver-'+AISettingsVer+'-RGB-'+DATE+'-'+TIME
          #catch empty dirs
          if len(STACKEDFILES)==0:
               print 'no files in, '+TIME+' skipping, and removing folder'
               try:
                    #shutil.rmtree(os.path.join(Stacked, DATE, TIME))
                    print "DELETING "+os.path.join(Stacked, DATE, TIME)+" to "+os.path.join(RGBd, DATE, AS2ed)
               except:
                    print "Can NOT Delete "+os.path.join(Stacked, DATE, TIME)+" to "+os.path.join(RGBd, DATE, AS2ed)
                    pass
                    continue
          else:
               print 'Found '+str(len(STACKEDFILES))+' stacked files in '+TIME+', let\'s do search for filter matches'
          #Prime current folder again, try to remove later with proper path & file name pasting
          cli.prime(DATE, TIME)
          #Clear previous and potentially stale values
          ColorFiles={}
          #
          #Find the files that match necessary filters for RGB'ing and assgin them to the dictionary
          #This helps us pull out the files to sharpen by color and then combine them later
          #
          for F in STACKEDFILES:
               matchR=re.search(RRegex, F)
               matchG=re.search(GRegex, F)
               matchB=re.search(BRegex, F)
               matchIR=re.search(IRRegex, F)
               if matchR:
                    #print 'R= '+F
                    ColorFiles['R']=[F,'']
               if matchG:
                    #print 'G= '+F
                    ColorFiles['G']=[F,'']
               if matchB:
                    #print 'B= '+F
                    ColorFiles['B']=[F,'']
               if matchIR:
                    #print 'IR= '+F
                    ColorFiles['IR']=[F,'']
          print
          #
          #List and then sharpen stacks from the sorting into dictionaries
          #
          print 'Sharpneing file:'
          stackcounter=1
          for color,ToBeSharped in ColorFiles.iteritems():
               print str(stackcounter)+' of '+str(len(ColorFiles))
               stackcounter=stackcounter+1
               print ToBeSharped[0]
               cli.sharp(ToBeSharped[0], DATE, TIME,AISettingsVer)
          #
          # relist dirs to find sharps for RGB'ing
          #
          STACKEDFILES=os.listdir(os.path.join(Stacked,DATE,TIME,'v10'))
          #
          #Append existing dictionary for sharps in the second (ie [1]) postion of the value / list
          #
          for F in STACKEDFILES:
               matchR=re.search(r'Ver-'+AISettingsVer+'-Drizzle15_.*-R.*', F)
               matchG=re.search(r'Ver-'+AISettingsVer+'-Drizzle15_.*-G.*', F)
               matchB=re.search(r'Ver-'+AISettingsVer+'-Drizzle15_.*-B.*', F)
               matchIR=re.search(r'Ver-'+AISettingsVer+'-Drizzle15_.*-IR.*', F)
               if matchR:
                    #print 'Ver'+AISettingsVer+'R= '+F
                    ColorFiles['R'][1]=F
               if matchG:
                    #print 'Ver'+AISettingsVer+'G= '+F
                    ColorFiles['G'][1]=F
               if matchB:
                    #print 'Ver'+AISettingsVer+'B= '+F
                    ColorFiles['B'][1]=F
               if matchIR:
                    #print 'Ver'+AISettingsVer+'IR= '+F
                    ColorFiles['IR'][1]=F
          #Now let\'s search the sharped files to make sure all R, G and B are present
          RGBSharp='Ver-'+AISettingsVer+'-RGB-'+DATE+'-'+TIME
          print 'Now let\'s search the sharped files to make sure all R, G and B are present'
          try:
               ColorFiles['R'] and ColorFiles['G'] and ColorFiles['B']!=0
               print '\nFound all the rgb!'
               cli.RGB(ColorFiles['R'][1],ColorFiles['G'][1],ColorFiles['B'][1],RGBSharp,DATE, TIME,Duration)
          except:
               print '\nNot all RGB FOUND, moving on'
               pass
          print
          print
          print 'Now copying and sorting all the sharped mono channels into common subdir'
          monocopier(AISettingsVer,TIME)
          #Move dones to 30-Sharped+RGB
          sharpmover('RGB-Raw-'+DATE+'-'+TIME+'.tif','raw',TIME)
          time.sleep(1)
          sharpmover(RGBSharp+'.tif','Ver'+AISettingsVer,TIME)
          time.sleep(5)
          #Move Times from 20-Stacked when done checking
          print '\n\nCopying:'
          try:
                os.makedirs(os.path.join(RGBd, DATE, AS2ed,TIME,Ver))
          except:
                e = sys.exc_info()
                print e      
          for P,S,F in os.walk(os.path.join(Stacked, DATE, TIME)):
                for f in F:
                        print f
                        shutil.copy(os.path.join(P,f),os.path.join(RGBd, DATE, AS2ed,TIME,Ver))
                        print ' to '+str(os.path.join(Stacked, DATE, TIME,Ver))
          print
          print 'Verifying final sharps are copied...'
          print ' found the final count is at least as large as the starting count'
          len(os.path.join(RGBd, DATE, AS2ed,TIME)) >= len(os.listdir(os.path.join(Stacked, DATE, TIME,Ver)))
          if len(os.path.join(RGBd, DATE, AS2ed,TIME)) >= len(os.listdir(os.path.join(Stacked, DATE, TIME,Ver))):
                try:
                        shutil.rmtree(os.path.join(Stacked, DATE, TIME))
                except:
                        e = sys.exc_info()
                        print e

     '''
     consider
     for currenttime in TIMES:
          if TIMES.index(currenttime) > 0:
               pTIME=TIMES[TIMES.index(currenttime)-1]
               mover...
          else:
               pass

     '''

     print '\nPython portions done, closing AstraImage'
     AI.terminate()
     print '\n closing Sikuli'
     proc.terminate()
     DATETIME()

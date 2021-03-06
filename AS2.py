#! /usr/bin/python

'''     20140427
        Proper rewrite of AS2 stacking / post stacking with os.walks


'''

import subprocess, time, os, re, shutil, datetime, time, xmlrpclib, sys
from datetime import datetime as dt
from datetime import date
#custom defs
import oslib, FCinfo

FCfiletype='avi'
cli = xmlrpclib.ServerProxy("http://127.0.0.1:1337",allow_none=True)
Sikuli='D:\\D-Permanent\\Software\\Win7Installs\\Sikuli\\runIDE.cmd'
Sikuliarg1='-r'
scriptname='C:\\Users\\miphilli\\Documents\\GitHub\\Planetary\\AS2.sikuli'
proc = subprocess.Popen([Sikuli,Sikuliarg1,scriptname])
time.sleep(15)

def AS2(AP,Drizzle):
        #
        # Variable defintions
        #
        Win7Disk='C:\\'
        C='D:\\'
        D='E:\\'
        FC=os.path.join(Win7Disk,'Personal\\A-Inbox\\FireCaptures\\')
        #FC=os.path.join('D:\\A-Inbox\\1-Corianders-primary')
        #FC=os.path.join('E:\\Personal\\A-Inbox\\1-Corianders-primary')
        Ver = 'v10'
        Stacks='D:\\B-Sorted\\Astronomy\\Planetary\\20-Stacked'
        # Set expiration for 60 days from time of script execution
        days45=datetime.timedelta(days=45)
        today = date.today()
        expDATE=str(today+days45)
        TEMP=os.path.join('E-Delete','FireCaptures-Expiring--'+expDATE)

        #
        # Code reuse Custom Defs
        #

        #This one finds the time in the ISO-formatted date string
        def TimeMatch(st):
                match=re.search(r'[0-9]+\_[0-9]', st) # WinJUPOS time format may use hhmm.s or hhmm_s change as needed for GTime match errors
                if match:
                        result = match.group()
                        return result
                else:
                        print "Not Found"


        #
        # Now let's go find the captures and or stacks
        #

        #for P,S,F in os.walk(os.path.join(FC)):
                


        # get list of planets and dates
        if not os.listdir(FC):
                print 'Looks like you don\'t have any new captures and could use some clear skies'
                sys.exit()
        else:
                for planet in os.listdir(FC):
                        DATES = os.listdir(os.path.join(FC,planet))
                        if not DATES:
                                print 'Looks like you don\'t have any new captures and could use some clear skies'
                        else:
                                for DATE in DATES:
                                        # Prevent null results
                                        if oslib.used_space(os.path.join(FC,planet,DATE)) == 0:
                                                print
                                                print
                                                print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
                                                print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
                                                print 'Found '+DATE+' is empty, please remove and fix this portion of the script'
                                                print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
                                                print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
                                                print
                                                subprocess.Popen('explorer '+os.path.join(FC,planet))
                                                sys.exit()
                                        else:
                                                print
                                                print
                                                print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
                                                print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
                                                print 'Looks like we\'ve got '+oslib.humanize_bytes(oslib.used_space(os.path.join(FC,planet,DATE)))+' worth of captures to stack in subdir '+DATE
                                                print ' C: has '+oslib.humanize_bytes(oslib.free_space(C)*1024*1024)+' free'
                                                print ' D: has '+oslib.humanize_bytes(oslib.free_space(D)*1024*1024)+' free'
                                                print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
                                                print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
                                                print
                                                try:
                                                        print 'Here\'s a list of all the FireCapture settings:'
                                                        FCinfo.parser(os.path.join(FC,planet,DATE),planet,DATE)
                                                except:
                                                        pass
                                                pass

                                        print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
                                        print


                                        # Get all capture runs into a list
                                        TIMES=os.listdir(os.path.join(FC,planet,DATE))

                                        #Counter
                                        count=1

                                        # Iterate over captures
                                        for TIME in TIMES:                                                
                                                print '========================================================='
                                                print "Working on "+TIME+" ("+str(count)+" of "+str(len(TIMES))+")"
                                                count=count+1
                                                print '========================================================='
                                                GTime=TIME
                                                '''
                                                # Get mid-timestamp of run and set variable
                                                for P,S,F in os.walk(os.path.join(FC,planet,DATE,TIME)):
                                                        print P
                                                        print S
                                                        print F
                                                        print
                                                        print 'Searching for midpoint time of catpure'
                                                        for f in F:
                                                                print '.ser' or '.avi' in f
                                                                if '.ser' or '.avi' in f:
                                                                        if '_G' or '-G' in f:
                                                                                print 'Setting Capture time to match the start of Green:'
                                                                                GTime=TimeMatch(f)                                                                                
                                                                        elif '_R' or '-R' in f:
                                                                                print 'Setting Capture time to match the start of RED as Green wasn\'t found:'
                                                                                GTime=TimeMatch(f)
                                                                else:
                                                                        print 'No capture videos found'
                                                                        GTime=TIME
                                                                        print
                                                '''
                                                FILES=os.listdir(os.path.join(FC,planet,DATE,TIME))
                                                # Compare AVI qty to TIF qty and get Green time
                                                AVIs=[]
                                                AVIs=[FILE for FILE in FILES if FILE.endswith(FCfiletype)]
                                                print AVIs
                                                print oslib.humanize_bytes(oslib.used_space(os.path.join(FC,planet,DATE,TIME)))
                                                print
                                                DONEs=[FILE for FILE in FILES if FILE.startswith('AS_')]
                                                # Test for presence of an AS2 subfolder and stack if needed (MAIN)
                                                # Consider a compare of stacks to captures for incompletes!
                                                if not DONEs:
                                                        AutoStakkert = subprocess.Popen('D:\\D-Permanent\\Dropbox\\5-Permanent\\Astronomy\\Software\\AutoStakkert\\AutoStakkert.exe')
                                                        print TIME+' needs to be AS2 Stacked'
                                                        time.sleep(5)
                                                        cli.AS2(os.path.join(FC,planet,DATE,TIME),AP,Drizzle)
                                                        print '\nDone stacking...searching for stacked files...\n'
                                                        FILES=os.listdir(os.path.join(FC,planet,DATE,TIME))
                                                        DONEs=[FILE for FILE in FILES if FILE.startswith('AS_')]
                                                        print 'Found stacked files in '+str(DONEs)+'\n..'
                                                        # Close AutoStakkert to close file handles - done in Sikuli atm
                                                        AutoStakkert.terminate()                                                                            
                                                # Copy stacked TIFs
                                                for P,S,F in os.walk(os.path.join(FC,planet,DATE,TIME)):
                                                        if 'AS_' in P:
                                                                print P
                                                                try:
                                                                        os.makedirs(os.path.join(Stacks,DATE,GTime+'-'+TIME,Ver))
                                                                except:
                                                                        pass
                                                                for f in F:
                                                                        print f
                                                                        print
                                                                        try:
                                                                                print ' Copying '+TIME+' stacked tifs to '+os.path.join(Stacks,DATE,GTime+'-'+TIME,Ver)                                               
                                                                                shutil.copy(os.path.join(P,f),os.path.join(Stacks,DATE,GTime+'-'+TIME,Ver))
                                                                        except:
                                                                                e = sys.exc_info()[0]
                                                                                print 'FAILED to copy '+TIME+'stacked tifs to '+os.path.join(Stacks,DATE,GTime+'-'+TIME,Ver)
                                                                                print 'Reason '+str(e)
                                                                                pass
                                                # Now verify the copy before archiving the originals
                                                print
                                                print ' Attemping to archive captures, checking if '+TIME+' was properly copied'
                                                # Simple test of Stacks folder
                                                try:
                                                        if os.listdir(os.path.join(Stacks,DATE,GTime+'-'+TIME,Ver)) > 0:
                                                                print ' Some stacks are there, now checking freespace to pick a disk to move captures to.'
                                                                print
                                                                try:
                                                                        if os.path.getsize(os.path.join(FC,planet,DATE,TIME)) < oslib.free_space(D):
                                                                                print 'Moving '+str(oslib.humanize_bytes(oslib.used_space(os.path.join(FC,planet,DATE,TIME))))\
                                                                                      +' of AVIs from '+TIME+' to '+os.path.join(D,TEMP,DATE,TIME)\
                                                                                      +' that has '+oslib.humanize_bytes(oslib.free_space(D)*1024*1024)+' free'
                                                                                shutil.move(os.path.join(FC,planet,DATE,TIME),os.path.join(D,TEMP,DATE))
                                                                        else:
                                                                                print 'Moving '+str(oslib.humanize_bytes(oslib.used_space(os.path.join(FC,planet,DATE,TIME))))\
                                                                                      +' of AVIs from '+TIME+' to '+os.path.join(C,'Personal',TEMP,DATE,TIME)\
                                                                                      +' that has '+oslib.humanize_bytes(oslib.free_space(C)*1024*1024)+' free'
                                                                                shutil.move(os.path.join(FC,planet,DATE,TIME),os.path.join(C,'Personal',TEMP,DATE))
                                                                except:
                                                                        print ' FAILED to move '+TIME+' stacked tifs to '+os.path.join(Stacks,DATE,GTime+'-'+TIME,Ver)
                                                                        e = sys.exc_info()[0]
                                                                        print 'Reason '+e
                                                                        pass
                                                        else:
                                                                print ' Files NOT copied properly!  Leaving AVIs in transit'
                                                                pass
                                                except:
                                                        print ' FAILED to find '+TIME+' stacked tifs to '+os.path.join(Stacks,DATE,GTime+'-'+TIME,Ver)
                                                        e = sys.exc_info()[0]
                                                        print e
                                                        pass


        try:
                AutoStakkert.terminate()
        except:
                print 'Can\'t close AutoStakkert2.exe'
                e = sys.exc_info()[0]
                print 'Reason '+str(e)
         
        proc.terminate()
                
'''
        # Clean up of capture folders when emptied
        if len(os.listdir(os.path.join(FC,planet,DATE))) == 0:
                print 'You are all done with this night\'s data!  Let\'s remove the folder '+DATE
                shutil.move(os.path.join(FC,planet,DATE),os.path.join(TEMP,DATE))
        else:
                print 'You might need to run this script again, not everything is clean in the subdir '+DATE
                pass
'''

        #File mover via defs?



        #os.popen('explorer '+os.path.join(Stacks,DATE))

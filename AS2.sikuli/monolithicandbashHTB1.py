from sikuli.Sikuli import *
import subprocess, sys, os, os.path, shutil
setAutoWaitTimeout(60)
myScriptPath = "/home/miphilli/Dropbox/5-Permanent/Sikuli/Linux/Astro/Planetary/v91"
if not myScriptPath in sys.path: sys.path.append(myScriptPath)
# Major rework on 20111128
#
# Define STATIC variables
#
# at f/29 on Akule:
#	Mars = 165 x 165
#	Saturn = 400 x 200
# to add sed: sed -f /home/miphilli/Dropbox/5-Permanent/BASH/Astronomy/Planetary/v10/prefsedscript
#NinoxCropX=165
NinoxCropX=input("Please enter CutX Dimention\n165 for Mars\n400 for Saturn")
#NinoxCropY=165
NinoxCropY=input("Please enter CutY Dimention\n165 for Mars\n200 for Saturn")
#NinoxScale=3
NinoxScale=input("Please enter upscale value")
#
TempWorkingDir = os.path.join(r'/Astronomy/Sorted/3-Unprocessed')
# set src $DATE variables for coriander captures
os.popen("ls /Astronomy/Transit/1-Corianders/ > /Astronomy/Sorted/2-Scratch/MAPninox-DATE.txt")
# set src $TIME variables for coriander captures
os.popen("ls /Astronomy/Transit/1-Corianders/20*/  | grep [0-9] > /Astronomy/Sorted/2-Scratch/MAPninox-TIME.txt")
#
sleep(5)
# set src PrefTime variables for parsing out cam values
#os.popen("ls /Astronomy/Transit/1-Corianders/20*/preferences/ > /Astronomy/Sorted/2-Scratch/MAPpref-TIME.txt")
#TempExpiringDir = os.path.join(r'/Astronomy/Sorted/2-Scratch/', DATE, TIME)
#
#
# Verify static directory structures and other static things
#
#os.popen("mkdir -p " + TempWorkingDir)
os.popen("mkdir -p /Astronomy/Sorted/2-Scratch")
os.popen("mkdir -p /Astronomy/Sorted/4-Temp\ Stacked/Solar\ System/")
os.popen("mkdir -p /Astronomy/Save/ProcessingTimes")
os.popen("chmod u+x -R /home/miphilli/Dropbox/5-Permanent/BASH/*")
#os.popen("rm -rf /Astronomy/Sorted/2-Scratch/MAPninox-????.txt*")
#os.popen("rm -rf /Astronomy/Sorted/2-Scratch/MAPpref-TIME.txt")
#
# Read captures from Transit folder
#
DATEFILE = open('/Astronomy/Sorted/2-Scratch/MAPninox-DATE.txt', "r")
TIMEFILE = open('/Astronomy/Sorted/2-Scratch/MAPninox-TIME.txt', "r")
#
# Open DATE for varaible
#
for D in DATEFILE:
	DATE = D.rstrip('\r\n')
#
# Open TIME for varaible and finalize VARIABLE variables
#
for T in TIMEFILE:
	TIME = T.rstrip('\r\n')
	print ("This is the Date: " + DATE + ", and this is the Time: " + TIME)
	#
	#Dynamic variables such as 2-Scratch, 4-Temp Stacked
	#
	ScratchDir = os.path.join(r'/Astronomy/Sorted/2-Scratch/', DATE, TIME)
	ScratchDirR = os.path.join(r'/Astronomy/Sorted/2-Scratch/', DATE, TIME, 'Rtop2000')
	ScratchDirG = os.path.join(r'/Astronomy/Sorted/2-Scratch/', DATE, TIME, 'Gtop2000')
	ScratchDirB = os.path.join(r'/Astronomy/Sorted/2-Scratch/', DATE, TIME, 'Btop2000')
	ScratchDirIR = os.path.join(r'/Astronomy/Sorted/2-Scratch/', DATE, TIME, 'IRtop2000')
	ScratchDirUV = os.path.join(r'/Astronomy/Sorted/2-Scratch/', DATE, TIME, 'UVtop2000')
	ScratchDirL = os.path.join(r'/Astronomy/Sorted/2-Scratch/', DATE, TIME, 'Ltop2000')

	Unprocessed = os.path.join(r'/Astronomy/Sorted/3-Unprocessed')

	StackedDir = os.path.join(r'/Astronomy/Sorted/4-Temp Stacked/Solar System/', DATE.rstrip('\r\n'), TIME.rstrip('\r\n'), 'v95')
	StackedDirAll = os.path.join(r'/Astronomy/Sorted/4-Temp Stacked/Solar System/', DATE.rstrip('\r\n'), 'all')
	D = int(DATE.rstrip('\r\n'))
	Dcalc = (D + 200)
	print ("Expires " + str(Dcalc))
	ExpiryDirCoriander = os.path.join(r'/Astronomy/Temp/Corianders-Expiring--', str(Dcalc), DATE.rstrip('\r\n'), 'Corianders')
	ExpiryDirNinoxed = os.path.join(r'/Astronomy/Temp/Corianders-Expiring--', str(Dcalc), DATE.rstrip('\r\n'), 'Ninoxed')
	print ExpiryDirCoriander

#Make Directories
	try:
		os.makedirs(ScratchDir)
	except os.error:
		print "Directory already exists, moving on..."#print str(DATELIST)
	try:
		os.makedirs(ScratchDirR)
	except os.error:
		print "Directory already exists, moving on..."#print str(DATELIST)
	try:
		os.makedirs(ScratchDirG)
	except os.error:
		print "Directory already exists, moving on..."#print str(DATELIST)
	try:
		os.makedirs(ScratchDirB)
	except os.error:
		print "Directory already exists, moving on..."#print str(DATELIST)
	try:
		os.makedirs(ScratchDirIR)
	except os.error:
		print "Directory already exists, moving on..."#print str(DATELIST)
	try:
		os.makedirs(ScratchDirUV)
	except os.error:
		print "Directory already exists, moving on..."#print str(DATELIST)
	try:
		os.makedirs(ScratchDirL)
	except os.error:
		print "Directory already exists, moving on..."#print str(DATELIST)
	try:
		os.makedirs(StackedDir)
	except os.error:
		print "Directory already exists, moving on..."#print str(DATELIST)
	try:
		os.makedirs(StackedDirAll)
	except os.error:
		print "Directory already exists, moving on..."#print str(DATELIST)
	try:
		os.makedirs(TempWorkingDir)
	except os.error:
		print "Directory already exists, moving on..."#print str(DATELIST)
	try:
		os.makedirs(Unprocessed)
	except os.error:
		print "Directory already exists, moving on..."#print str(DATELIST)


#Log times
	os.popen("touch /Astronomy/Save/ProcessingTimes/" + DATE.rstrip('\r\n') + ".txt")
	os.system("echo Time = " + TIME.rstrip('\r\n') + " >> /Astronomy/Save/ProcessingTimes/" + DATE.rstrip('\r\n') + ".txt")
	os.system("echo NinoxScale = " + NinoxScale + " >> /Astronomy/Save/ProcessingTimes/" + DATE.rstrip('\r\n') + ".txt")
	os.system("echo	Ninox started: >> /Astronomy/Save/ProcessingTimes/" + DATE.rstrip('\r\n') + ".txt")
	os.system("	date >> /Astronomy/Save/ProcessingTimes/" + DATE.rstrip('\r\n') + ".txt")
# Tracer files
	os.popen("touch " + ScratchDir + "/" + DATE.rstrip('\r\n') + "-" + TIME.rstrip('\r\n') + ".txt")
	os.popen("touch " + Unprocessed + "/" + DATE.rstrip('\r\n') + "-" + TIME.rstrip('\r\n') + ".txt")
		
#
## NINOX
#
# NINOX OPTIONS
#
	MAPNinox=("/Astronomy/5-Permanent/Software/ninox/ninox -display -cutx=" + str(NinoxCropX) + " -cuty=" + str(NinoxCropY) + " " + "-qtrim -qestimator -qrenumber -resample=" + str(NinoxScale) + "/1 -outdir=/Astronomy/Sorted/2-Scratch/" + DATE.rstrip('\r\n') + "/" + TIME.rstrip('\r\n') + " /Astronomy/Transit/1-Corianders/" + DATE.rstrip('\r\n') + "/" + TIME.rstrip('\r\n'))
#	MAPNinox=("/Astronomy/5-Permanent/Software/ninox/ninox -display -nocutout -qtrim -qestimator -qrenumber -resample=" + str(NinoxScale) + "/1 -outdir=/Astronomy/Sorted/2-Scratch/" + DATE.rstrip('\r\n') + "/" + TIME.rstrip('\r\n') + " /Astronomy/Transit/1-Corianders/" + DATE.rstrip('\r\n') + "/" + TIME.rstrip('\r\n'))
#	gnome-terminal --title=NINOX --geometry=50x12 -x /home/miphilli/Dropbox/5-Permanent/BASH/Astronomy/Planetary/v9/ninoxloop2x.sh
#	MAPNinoxCMD = ("gnome-terminal --title=NINOX --geometry=50x12 -x /Astronomy/5-Permanent/Software/ninox/ninox -display -cut=150 -qestimator -qrenumber -resample=2/1 -outdir=/Astronomy/Sorted/2-Scratch/" + DATE.rstrip('\r\n') + "/" + TIME.rstrip('\r\n') + " /Astronomy/Transit/1-Corianders/" + DATE.rstrip('\r\n') + "/" + TIME.rstrip('\r\n'))
#
	os.system(MAPNinox)
#
	sleep(3)
	os.system("echo	Ninox ended: >> /Astronomy/Save/ProcessingTimes/" + DATE.rstrip('\r\n') + ".txt")
	os.system("	date >> /Astronomy/Save/ProcessingTimes/" + DATE.rstrip('\r\n') + ".txt")
	os.system("echo  >> /Astronomy/Save/ProcessingTimes/" + DATE.rstrip('\r\n') + ".txt")
#
#Post-Ninox BASH move
# This also moves the preferences files
# Use old bash method to sort cropped files to Xtop2000
#
	os.system("/home/miphilli/Dropbox/5-Permanent/BASH/Astronomy/Planetary/v9/Ntop2kmoveallHTB.sh " + DATE.rstrip('\r\n') + " " + TIME.rstrip('\r\n') + " " + str(Dcalc))
#
#
# Run AS2
#
#	import AS2
#Define Watchdog variables
	CMD = "top -b -n 1 | gawk '/Stakkert/ {print $9}'"
	test = True
	cpuMax = 2
	#Verify cleanup of workspace
	os.popen("killall workrave")
	os.popen("killall cairo-dock")
	os.popen("killall 88-AutoStakkert.exe")
	sleep(10)
	#
	# BATCH all Xtop2000
	#
	os.system("echo	AS2 started " + TIME.rstrip('\r\n') + " >> /Astronomy/Save/ProcessingTimes/" + DATE.rstrip('\r\n') + ".txt")
	os.system("	date >> /Astronomy/Save/ProcessingTimes/" + DATE.rstrip('\r\n') + ".txt")
	os.system("nautilus /Astronomy/Sorted/2-Scratch/" + DATE + "/" + TIME + " --geometry 1600x475+76+575")
	os.popen("/home/miphilli/Documents/Dropbox/5-Permanent/Shortcuts/PlanetaryProcessing/v95/88-AutoStakkert.exe&")
	sleep(10)
	switchApp("AutoStakkert")
#	wait(Pattern("OutputImageG.png").similar(0.59))
	sleep(10)
	switchApp(TIME)
#	wait(Pattern("Bt0p2000Gt0p.png").similar(0.80))
#	switchApp("3-Unprocessed - File Browser")
	sleep(3)
	type("a",KEY_CTRL)
#	sleep(5)
#	paste('*')
#	sleep(5)
#	type(Key.ENTER)
	sleep(5)
	dragDrop(Pattern("Rt0p2000-1.png").similar(0.98), "1Open.png")
	sleep(60)
	click(Pattern("2bAnalyzeRef.png").targetOffset(0,-58))
	while True:
		AS2CPU = os.popen(CMD).readlines()
		cpu = float(AS2CPU[0])
		if test: print cpu
		if cpu < cpuMax : break
		wait(5)
		print(AS2CPU)
	switchApp("Stakkert")
	wait("Bufferingand.png")
	sleep(2)
	click(Pattern("Dunfurgetset.png").similar(0.00).targetOffset(-18,16))
	sleep(3)
	while True:
		AS2CPU = os.popen(CMD).readlines()
		cpu = float(AS2CPU[0])
		if test: print cpu
		if cpu < cpuMax : break
		wait(5)
		print(AS2CPU)
	os.system("echo	AS2 end: >> /Astronomy/Save/ProcessingTimes/" + DATE + ".txt")
	os.system("	date >> /Astronomy/Save/ProcessingTimes/" + DATE + ".txt")
	os.system("echo  >> /Astronomy/Save/ProcessingTimes/" + DATE.rstrip('\r\n') + ".txt")
	os.system("echo  >> /Astronomy/Save/ProcessingTimes/" + DATE.rstrip('\r\n') + ".txt")
	click(Pattern("CulurAdvance.png").similar(0.00).targetOffset(212,-88))
	switchApp(TIME)
	sleep(1)
	type(" ",KEY_ALT)
	sleep(1)
	type("c")
#
# Run AstraImage subroutine
#
#	import AstraImage
#
# Run Gimp subroutine
#
#	import gimp
#
# Move processed stack goods to 4-Temp Stack
#
	os.system("/home/miphilli/Dropbox/5-Permanent/BASH/Astronomy/Planetary/v9/processedmove.sh " + DATE.rstrip('\r\n') + " " + TIME.rstrip('\r\n') + " " + str(Dcalc))
#
#
#popup("DONE")
os.system("gedit /Astronomy/Save/ProcessingTimes/" + DATE + ".txt")
#os.system("pmi action suspend")
#END
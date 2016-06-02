import sys
import os
#sys.path.append("C:\\root_v5.34.34\\bin")		# only used in some Windows system, it has to do with ROOT behavior
from ROOT import *
import imp
import time
import numpy as np
import matplotlib.pyplot as plt
import math
sqrt = math.sqrt


from ROOT import TFile, TTree 			
from array import array				

# Hard coded variable used throughout the code
points_per_event=500
guards=[0,80,125,250,375,500]


def ReadList(listname):
	readd_list=[]
	with open(listname, 'r') as f:
		readd_list = [line.rstrip('\n') for line in f]	
	return readd_list




def WriteList(input, filename):
	with open("runfiles/ascii/"+filename+".dat", 'w') as f:
			for s in input:
				f.write(str(s) + '\n')


def SelectRunFile():
	run_number = raw_input("\nPlease enter the desired RUN number \nRun #: ")
	run_number = str(run_number)
	runfiles_available = os.listdir("runfiles")
	runfile = ''
	for item in runfiles_available:
		if '_'+run_number in item:
			runfile = item
	response = 'y'
	if runfile != '':
		# response = raw_input("Is "+runfile+" the correct runfile? : ")
		if response == 'y' :
			return runfile
	else:
		print "No such runfile present."
		raw_input("Press Enter to continue...")
		sys.exit()






def RunfileProcessing(filename):
	i=0
	print "Processing stage #1 for runfile "+filename
	f = open("runfiles/"+filename,'r')
	data=[]

	for line in f.xreadlines():
		if i<13:
			i+=1
			pass
		else:
			data.append(float(line))
	f.close()
	print "We have ", len(data)/points_per_event, " events in this runfile"
	return data

# Currently not being used, implement this for exceptions.
def SelectTree():
	# # First of all, we need to test if the ROOT file exists, and if not, create it.
	# treename = "..."
	# print "is it here?"
	# if TFile( '...', 'open' ):
		# Treefile = ROOTfile.Get('...')
	# else:
		# Treefile = TFile( "'...'.root", 'open' ):

	pass

# Shifts a list of X elements by a positive or negative number, maintaining size and adding zeroes.
def ShiftList_horizontally(list, shift):
	shifted_list=[]
	shift=int(shift)
	print "Shift input list horizontally, by", shift
	for i in xrange(len(list)):
		shifted_list.append(0)
	if shift > 0:
		for i in xrange(len(list)-shift):
			shifted_list[i+shift]=list[i]
	elif shift < 0:
		for i in xrange(len(list)+shift):
			shifted_list[i]=list[i-shift]
	elif shift==0:
		return list
	return shifted_list

# Shifts a list of Y elements, by adding or subtracting the same value for all elements.
# eg we can use this to calibrate for a constant offset.
def ShiftList_vertically(list, shift):
	print "Shift input list vertically, by", shift
	shifted_list=[]
	for i in xrange(len(list)):
		shifted_list.append(list[i]+shift)
	return shifted_list


def SelectRunBackground():
	run_number = raw_input("Please enter event run#: ")
	background_number = raw_input("Please enter background run#: ")
	return run_number, background_number


# Inputs -- Run#, Type of tree, Content to fetch
# Outputs-- Just a list for now
def FetchDataPoints(run, type, event):				# This actually works. Need to test case of event0 aka x'x axis
	if event == '0':					            # Construct a x'x axis			
		list=[]
		for i in xrange(points_per_event):
			list.append(i)
		return list
		pass
		
	
	ROOTfilename = "Run_"+run+"_file.root"
	ROOTfile = TFile (ROOTfilename, 'open')
	# print TFile (ROOTfilename, 'open')				# Check if object is loaded on memory

	treename = "Run_" + run + "_" + type + ".root"
	tree1=ROOTfile.Get(treename)
        # print ROOTfile.Get(treename)					# Check if object is loaded on memory

	# Type of data we request from the tree
	if type == "stats":
		leaf = "Run_"+run+"_"+event
	elif type == "events":
		leaf = "Run_"+run+"_event"+event
	# print "Treename is", treename
	# print "leafname is", leaf
	j=0
	list=[]
	my_string = 'list.append(item.'+leaf+')'
	for item in tree1:
		# print type(event)
		# print type(event.Run_23_mean)
		# print event.leaf																	# for item in tree : print event.leaf
		exec my_string																        # maybe we will need to parse this somehow
		j+=1
	# print "Datapoints fetched -", j, '. From treename', treename, 'and leaf', leaf
	# print "len of returned list", len(list)
	return list	

def AdditionalBranches():
	
	Backrun = raw_input("We need a background run file to calculate additional info \nPlease enter a run-number that has been used to measure the background in similar conditions-setups \nRun #: ")
	Backrun = str(Backrun)
	Eventrun = runfile[-6:-4]

	# The following 50 lines of code are somewhat retarded, and should be changed to some (exec) function.
	# Due to PyROOT behaving strangely, we leave them to be for now
	Treefile1.Branch(runid+"_mean", InputArray1, runid+"_mean"+'/D' )
	Treefile1.Branch(runid+"_rms", InputArray2, runid+"_rms"+'/D' )
	Treefile1.Branch(runid+"_meanerror", InputArray3, runid+"_meanerror"+'/D' )
	
	InputArray6 = np.zeros(1, dtype=float)
	InputArray7 = np.zeros(1, dtype=float)
	InputArray8 = np.zeros(1, dtype=float)
	InputArray9 = np.zeros(1, dtype=float)
	InputArray10 = np.zeros(1, dtype=float)
	InputArray11 = np.zeros(1, dtype=float)
	InputArray12 = np.zeros(1, dtype=float)
	InputArray13 = np.zeros(1, dtype=float)
	InputArray14 = np.zeros(1, dtype=float)
	InputArray15 = np.zeros(1, dtype=float)
	InputArray16 = np.zeros(1, dtype=float)
	InputArray17 = np.zeros(1, dtype=float)
	
	# Create 11(?) branches for the first tree, for the Mean, RMS, charge, peak distribution, pulse height histograms, in each area.
	br4 = Treefile3.Branch(runid+"_Area1mean"+"_BG"+Backrun, InputArray6, runid+"_Area1mean"+"_BG"+Backrun+'/D' )
	br5 = Treefile3.Branch(runid+"_Area1rms"+"_BG"+Backrun, InputArray7, runid+"_Area1rms"+"_BG"+Backrun+'/D' )
	
	br6 = Treefile3.Branch(runid+"_Area2mean"+"_BG"+Backrun, InputArray8, runid+"_Area2mean"+"_BG"+Backrun+'/D' )
	br7 = Treefile3.Branch(runid+"_Area2rms"+"_BG"+Backrun, InputArray9, runid+"_Area2rms"+"_BG"+Backrun+'/D' )
	
	br8 = Treefile3.Branch(runid+"_SignalArea_Charge"+"_BG"+Backrun, InputArray10, runid+"_SignalArea_Charge"+"_BG"+Backrun+'/D' )
	br9 = Treefile3.Branch(runid+"_SignalArea_PulseHeight"+"_BG"+Backrun, InputArray11, runid+"_SignalArea_PulseHeight"+"_BG"+Backrun+'/D' )
	br10 = Treefile3.Branch(runid+"_SignalArea_PeakDistr"+"_BG"+Backrun, InputArray12, runid+"_PeakDistr"+"_BG"+Backrun+'/D' )

	
	br11 = Treefile3.Branch(runid+"_Area4mean"+"_BG"+Backrun, InputArray13, runid+"_Area4mean"+"_BG"+Backrun+'/D' )
	br12 = Treefile3.Branch(runid+"_Area4rms"+"_BG"+Backrun, InputArray14, runid+"_Area4rms"+"_BG"+Backrun+'/D' )

	br13 = Treefile3.Branch(runid+"_Area5mean"+"_BG"+Backrun, InputArray15, runid+"_Area5mean"+"_BG"+Backrun+'/D' )
	br14 = Treefile3.Branch(runid+"_Area5rms"+"_BG"+Backrun, InputArray16, runid+"_Area5rms"+"_BG"+Backrun+'/D' )


	EventData=[]
	EventData_minusBG=[]
	rms_allevents0=[]
	mean_allevents0=[]
	rms_allevents1=[]
	mean_allevents1=[]
	rms_allevents2=[]
	mean_allevents2=[]
	rms_allevents3=[]
	mean_allevents3=[]
	rms_allevents4=[]
	mean_allevents4=[]


	peak_list=[]
	ipeak_list=[]


	t = time.time()
	# do stuff
	# for now, we keep this, as it's only used once.
	BackgroundDataMean = FetchDataPoints(Backrun, "stats", "mean")
	shift_hor = raw_input("\nShift our background horizontally by bins#:")
	if shift_hor!=0:
		BackgroundDataMean=ShiftList_horizontally(BackgroundDataMean, shift_hor)

	# if something breaks, this is at fault.
	for i in xrange(events_in_file-2):				# use this for full parsing
		if i%1000==0:
			print "Now on entry, ", i
		rms=0
		EventData=[]
		EventData_minusBG=[]
		for u in xrange(points_per_event):
			EventData.append(rundata[i*points_per_event+u])
            
		# Instead of Fetching the data every time, from a TTree, let's try to read them from the list we already got... 200 events from the TTree needed 36 minutes to get fetched and compiled. Thats really really bad.
		# 2.051 seconds for 200 events, when reading from the 'runlist' variable this is like MUCH better.
		# print "len(EventData) is", len(EventData)
		# EventData = FetchDataPoints(Eventrun, "events", str(i))
		for x in xrange(points_per_event):
			EventData_minusBG.append(EventData[x]-BackgroundDataMean[x])
		
		# guards=[0,80,125,250,375,500]
		for q in xrange(5):
			lower_limit = q
			upper_limit = q+1
			sum1=0
			sum2=0
			peak=0
			ipeak=0
			nsum=0
			p=guards[lower_limit]
			while p<guards[upper_limit]:
				sum1=sum1+EventData_minusBG[p]
				sum2=sum2+EventData_minusBG[p]**2
				nsum+=1
				if peak>EventData_minusBG[p]:
					peak=EventData_minusBG[p]
					ipeak=p
				p+=1
			sum1=sum1/nsum
			sum2=sum2/nsum
			rms=( sqrt(sum2 - sum1**2) )
			mean01=sum1
			if q==0:
				rms_allevents0.append(rms)	
				mean_allevents0.append(mean01)
			elif q==1:
				rms_allevents1.append(rms)	
				mean_allevents1.append(mean01)
			#=====signal area starts here
			elif q==2: 	
				rms_allevents2.append(rms)
				charge=-mean01*nsum*0.2*1000/50
				if charge<0:
					charge=0
				mean_allevents2.append(charge)
				peak_list.append(peak)
				ipeak_list.append(ipeak)
			#=====signal area ends here
			elif q==3:
				rms_allevents3.append(rms)	
				mean_allevents3.append(mean01)
			elif q==4:
				rms_allevents4.append(rms)	
				mean_allevents4.append(mean01)

	print "Time elapsed in the AdditionalBranches func = "+ str(time.time() - t)	

	
	items = len(mean_allevents0)
	print len(rms_allevents0), "data in histogram"
	print len(peak_list), "data in histogram"
	for i in xrange(items):					# change all this to an exec statement
		InputArray6[0] = mean_allevents0[i]
		InputArray7[0] = rms_allevents0[i]
		InputArray8[0] = mean_allevents1[i]
		InputArray9[0] = rms_allevents1[i]
		InputArray10[0]= mean_allevents2[i]
		InputArray11[0]= peak_list[i]
		InputArray12[0]= ipeak_list[i]
		InputArray13[0]= mean_allevents3[i]
		InputArray14[0]= rms_allevents3[i]
		InputArray15[0]= mean_allevents4[i]
		InputArray16[0]= rms_allevents4[i]
		br4.Fill()
		br5.Fill()
		br6.Fill()
		br7.Fill()
		br8.Fill()
		br9.Fill()
		br10.Fill()
		br11.Fill()
		br12.Fill()
		br13.Fill()
		br14.Fill()
		Treefile3.SetEntries()
		
	print len(mean_allevents0), "data in histograms"

	
	
#========================================================================
#===	all imports, declarations	=================================
#===	 and dependencies, above these lines	=========================
#========================================================================



#=================================================================
#=================================================================
#=================================================================
#=========	CodE	 StarTs	 HeRe	==============================
#=================================================================
#=================================================================
#=================================================================

gROOT.Reset()
t = time.time()
# We will try to outline the steps towards creating what we wish.

# We need to explicitly define the arrays we're gonna use.
# del <var> to delet variables we're no longer gonna use.
# Try to keep all declarations consistent and in one place.
InputArray1 = np.zeros(1, dtype=float)
InputArray2 = np.zeros(1, dtype=float)
InputArray3 = np.zeros(1, dtype=float)
InputArray4 = np.zeros(1, dtype=float)
InputArray500 = np.zeros(500, dtype=float)

# Selects the runfile we need.
runfile = SelectRunFile()
# # print runfile
# Completes the Stage1 procssing of the runfile
rundata = RunfileProcessing(runfile)

# Variable used throughout the code.
events_in_file = len(rundata)/points_per_event

# Calculate statistical values, looping the events bin-by-bin
mean=[]
meansquared=[]
for x in xrange(points_per_event):
	sum=0.
	sumsquares=0.
	#for each separate event
	#calculate <x> and <x^2>
	for i in xrange(events_in_file):
		sum = sum + rundata[i*points_per_event+x]
		sumsquares = sumsquares + rundata[i*points_per_event+x]**2
	mean.append(sum/events_in_file)
	meansquared.append(sumsquares/events_in_file)

rms=[]
for x in xrange (points_per_event):
	rms.append(sqrt(meansquared[x]-mean[x]**2))

meanerror=[]
for x in xrange (points_per_event):
	meanerror.append(sqrt(meansquared[x]-mean[x]**2)/sqrt(events_in_file))


# ASCII output, for future reference.
WriteList(mean, runfile[:-4]+"_Mean")
WriteList(meansquared, runfile[:-4]+"_MeanSquared")
WriteList(rms, runfile[:-4]+"_RMS")
WriteList(meanerror, runfile[:-4]+"_MeanError")


xx = np.arange(0., points_per_event, 1)

# ls = 'dotted'
# plt.errorbar(xx, mean, xerr=0, yerr=rms, ls=ls, color='blue')
# plt.errorbar(xx, mean, xerr=0, yerr=meanerror, ls=ls, color='red')
# plt.plot(xx, mean)
# plt.plot(xx, rms)
# plt.show()

shifted_mean=[]

runid="Run_" + runfile[-6:-4]				# If we're gonna have more than 100 runs, we should change this.
											# The program is too dependent on this, be careful.
ROOTfilename = runid+"_file.root"

print ROOTfilename
ROOTtreename_stats  = runid+"_stats.root"
ROOTtreename_events = runid+"_events.root"
ROOTtreename_extra  = runid+"_extra.root"

# Create a ROOT TTree file, and overwrite if it already exists.
# ROOTfile = TFile (ROOTfilename, 'recreate')
ROOTfile = TFile (ROOTfilename, 'update')

# Create three trees, one for each purpose 
Treefile1 = TTree (ROOTtreename_stats, 'treeforstats')
Treefile2 = TTree (ROOTtreename_events, 'treeforevents')
Treefile3 = TTree (ROOTtreename_extra, 'treeforevents')

# Treefile1 = ROOTfile.Get(ROOTtreename_stats)
# Treefile1 = ROOTfile.Get(ROOTtreename_events)
# Treefile1 = ROOTfile.Get(ROOTtreename_extra)

# Create 3 branches for the first tree, for the Mean, RMS, MeanError values in a bin-by-bin basis.
br1=Treefile1.Branch(runid+"_mean", InputArray1, runid+"_mean"+'/D' )
br2=Treefile1.Branch(runid+"_rms", InputArray2, runid+"_rms"+'/D' )
br3=Treefile1.Branch(runid+"_meanerror", InputArray3, runid+"_meanerror"+'/D' )

for i in xrange(points_per_event):
	InputArray1[0]=mean[i]
	InputArray2[0]=rms[i]
	InputArray3[0]=meanerror[i]
	br1.Fill()
	br2.Fill()
	br3.Fill()
	Treefile1.SetEntries()


dict1={}
for x in xrange(events_in_file):
	dict1[x]=[]
	for u in xrange (points_per_event):
		dict1[x].append(rundata[points_per_event*x+u])


# We use this to make the x'x axis
dict1[events_in_file]=[]
for i in xrange(points_per_event):
	dict1[0][i]=i											# Multiply this line by time factor



for i in xrange(events_in_file):					# Use this line for full parsing.
	InputArray5 = np.zeros(1, dtype=float)
	a = Treefile2.Branch(runid+"_event"+str(i), InputArray5, runid+"event"+str(i)+'/D')
	for j in xrange(points_per_event):
		InputArray5[0] = dict1[i][j]
		# a.Fill()
		try:
			a.Fill()
		except:
			# ROOTfile.Write()
			print "encountered an error on event", i
			print "I'm gonna wait for 30s"
			time.sleep(15)
			print "Waited 30s. On to the next?"
			# This isn't working as intended.
			# ROOTfile = TFile (ROOTfilename, 'close')
			# print "I'm gonna wait for 30s"
			# time.sleep(15)
			# gROOT.Reset()
			# ROOTfile = TFile (ROOTfilename, 'open')
			i+=1
	if i%1000==0:
		print i
	# dict1.pop(i, None)
	# del dict[i]
	Treefile2.SetEntries()																# smh smh . . . 
	# dict1.pop(i, None)
	del dict1[i]

dict1 = None
del dict1

print "Time elapsed writing primary trees = "+ str(time.time() - t)
#========================================================================
#========================================================================
#========================================================================
#===	Separate the code after these	=================================
#========================================================================
#========================================================================
#========================================================================
	
ROOTfile.Write()
response = raw_input(" \nWould you like to calculate additional data, such as the Charge, Pulse Heigh and Peak Distribtions?")
if response == 'y':
	AdditionalBranches()
ROOTfile.Write()


f = TBrowser()



#========================================================================
#=========	by Tsilias Paschalis (AuTh)	=================================
#========================================================================
#===	Section.80	=====================================================
#========================================================================
#========================================================================
#========================================================================

raw_input("Press Enter to continue...")
print "Done"

import sys
import os
sys.path.append("C:\\root_v5.34.34\\bin")
from ROOT import *
import imp
import time
import numpy as np
import matplotlib.pyplot as plt
import math


from ROOT import TFile, TTree 			
from array import array				

# Variable used throughout the code
# It should only be changed by hand, when needed
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


def SelectRunFiles():
	# run_number = raw_input("Please enter the desired RUN number \n #: ")
	# run_number = str(run_number)
	run_number='23'
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
	# for line in f.read().split('\n'):
	# data = [line.strip() for line in open("runfiles/"+filename 'r')]

	for line in f.xreadlines():
		if i<13:
			i+=1
			pass
		else:
			data.append(float(line))
	f.close()
	print "We have ", len(data)/points_per_event, " events in this runfile"
	return data


def SelectTree():
	# # First of all, we need to test if the ROOT file exists, and if not, create it.
	# treename = "..."
	# print "is it here?"
	# if TFile( '...', 'open' ):
		# Treefile = ROOTfile.Get('...')
	# else:
		# Treefile = TFile( "'...'.root", 'open' ):

	pass


def ShiftList_horizontally(list, shift):
	shifted_list=[]
	shift=int(shift)
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
	print "Shifted input list horizontally, by", shift
	return shifted_list


def ShiftList_vertically(list, shift):
	print "Shift input list vertically, by", shift
	shifted_list=[]
	for i in xrange(len(list)):
		shifted_list.append(list[i]+shift)
	return shifted_list


def SelectRunBackground():
	run_number = raw_input("Please enter event run#: ")
	background_number = raw_input("Please enter background run#: ")
	return str(run_number), str(background_number)


# Inputs -- Run#, Type of tree, Content to fetch
# Outputs-- Just a list for now
def FetchDataPoints(run, type, event):									# This actually works. Need to test case of event0 aka x'x axis
	if event == '0':													# for some reason, if i call event0 from the code, it's erroneous.
		list=[]
		for i in xrange(points_per_event):
			list.append(i)
		return list
		pass
	
	ROOTfilename = "Run_"+run+"_file.root"
	ROOTfile = TFile (ROOTfilename, 'open')
	# print TFile (ROOTfilename, 'open')								# Check if object is loaded on memory

	treename = "Run_" + run + "_" + type + ".root"
	tree1=ROOTfile.Get(treename)
	# print ROOTfile.Get(treename)										# Check if object is loaded on memory

	if type == "stats":
		leaf = "Run_"+run+"_"+event
	elif type == "events":
		leaf = "Run_"+run+"_event"+event
	if type == "extra":
		leaf = "Run_"+run+"_"+event
	# print "Treename is", treename
	# print "leafname is", leaf
	j=0
	list=[]
	my_string = 'list.append(item.'+leaf+')'
	for item in tree1:
		# print type(event)
		# print type(event.Run_23_mean)
		# print event.leaf																	# for item in tree : print event.leaf
		exec my_string																# maybe we will need to parse this somehow
		j+=1
	# print "Datapoints fetched -", j, '. From treename', treename, 'and leaf', leaf
	# print "len of returned list", len(list)
	return list
	

#========================================================================
#===	all imports, declarations	=====================================
#===	 and dependencies, above these lines	=========================
#========================================================================




#========================================================================
#===	Example 4	=====================================================
#========================================================================

# # First Application
# gROOT.Reset()

# # Create a new canvas, and customize it.
# c1 = TCanvas( 'c1', 'Dynamic Filling Example', 200, 10, 700, 500 )
# c1.SetFillColor( 0 )
# c1.GetFrame().SetFillColor( 10 )
# c1.GetFrame().SetBorderSize( 6 )
# c1.GetFrame().SetBorderMode( -1 )

# # Create a histogram
# # Taken from example
# hpx    = TH1F( 'hpx', 'This is an example charge distribution', 100, 0.00001, 2)

# for i in xrange(len(readd_list)):
	# ChargeNTuple.Fill(float(readd_list[i]))
# ChargeTree.Fill()
	
	
# for item in readd_list:	
	# hpx.Fill(float(item))
# RunXXFile.Write()

# # hpx.Fit("gaus")
# # hpx.GetMean
# # print "-->", gaus.GetParameter(0)
# # print "-->", gaus.GetParameter(1)
# # print "-->", gaus.GetParameter(2)

# # hpx.Draw()
# c1.Modified()
# c1.Update()
# # t = TBrowser()
# raw_input("Press Enter to continue...")


#=================================================================
#=================================================================
#=========	CodE	 StarTs	 HeRe	==============================
#=================================================================
#===	There are 3 sections in the code.	====================== 
#===	No new data is being produced	==========================
#===	That means, we're only using existing ROOT files	======
#=================================================================
#===	Section 1	==============================================
#===	outputs the Mean event value, w/ removed background	======
#===	and its related errors (rms)	==========================
#===	It will also calculate the ratio of the selected files	==
#===	that is useful when comparing background runfiles	======
#=================================================================
#===	Section 2	==============================================
#===	can output any event, with its background removed	======
#===	and all related statistical error	======================
#=================================================================
#===	Section 3	==============================================
#===	has statistical data, tallied by areas we've split	======
#===	our signal in. It also provides data about	==============
#===	the Charge, PulseHeight and Peak Distribution	==========
#===	in a small area near our signal	==========================
#===	Finally, it uses the surrounding areas to calculate	======
#===	any baseline offset we need to include in our calculations
#=================================================================
#=================================================================
#=================================================================
#=================================================================

gROOT.Reset()
events_in_file = 40
#We somehow need to either 
#a) read the number of leaves on the Events tree,
#b) read the whole ascii file again or
#c) make a separate ascii/leaf with only such extra information
	
# # Create a new canvas, and customize it.
# c1 = TCanvas( 'c1', 'Event example', 200, 10, 700, 500 )
# c1.SetFillColor( 0 )
# c1.GetFrame().SetFillColor( 10 )
# c1.GetFrame().SetBorderSize( 6 )
# c1.GetFrame().SetBorderMode( -1 )


# Section 1
# These two lines need to bbe filled before we carry on.
xx=FetchDataPoints('18', 'events', '0')							# Anything with flag '0' gets the x'x axis
Eventrun, Backrun = SelectRunBackground()

SignalDataMean = FetchDataPoints(Eventrun, "stats", "mean")
BackgroundDataMean = FetchDataPoints(Backrun, "stats", "mean")
RMS_Mean = FetchDataPoints(Eventrun, "stats", "rms")
# print "len of signal and bg means is", len(SignalDataMean)
# print len(SignalDataMean)==len(BackgroundDataMean)
MeanError=[]
RMS=[]

shift_hor = raw_input("Shift our background horizontally by bins#: ")
if shift_hor!=0 or shift_hor != '':
	BackgroundDataMean=ShiftList_horizontally(BackgroundDataMean, shift_hor)


SignalDataMean_minusBG=[]
Ratio=[]
times_the_ratio_is_not_good=0
for i in xrange(points_per_event):
	SignalDataMean_minusBG.append(SignalDataMean[i] - BackgroundDataMean[i])
	if BackgroundDataMean[i] != 0 :
		Ratio.append(SignalDataMean[i]/BackgroundDataMean[i])
	else:
		Ratio.append(1)
		times_the_ratio_is_not_good+=1

# print "Signal minus bg len is ", len(SignalDataMean_minusBG)
# print "Signal minus bg len is ", len(Ratio)



# We can now plot sth like
# plt.title('All events - Mean ==== Background - Mean === mean w/ removed background')
# plt.title('All events - Ratio of one input vs another - Used in background checking')
# We should also define the vertical lines.




c1 = TCanvas("c1","A Simple Graph with error bars",200,10,700,500);
c1.SetFillColor(42)
c1.SetGrid()
c1.GetFrame().SetFillColor(21)
c1.GetFrame().SetBorderSize(12)
n=len(SignalDataMean_minusBG)

x_errors=[]
for i in xrange(n):
	x_errors.append(0.)
x  = array( 'f', xx )
ex = array( 'f', x_errors)
y  = array( 'f', SignalDataMean_minusBG)
ey = array( 'f', RMS_Mean )

if n == len(xx):
	print "\n \nWe're good to go"
# create the TGraphErrors and draw it
	gr = TGraphErrors(n,x,y, ex, ey)
	gr.SetTitle("Mean Event values, w/ rms errorbars.")
	gr.SetMarkerColor(4)
	gr.SetMarkerStyle(21)
	gr.Draw("ALP")
	c1.Update();

print "Section 1 - Finished"

# Section 2 
# We select an event and have its points plotted, along with the removed background
print "\n \nSection 2 - Started"

response = raw_input("Please enter event#: ")
while response!="0":
	EventData=[]
	# fetch 500 data for this event only
	EventData = FetchDataPoints(Eventrun, 'events', str(response))
	EventData_minusBG=[]
	for i in xrange(points_per_event):
		EventData_minusBG.append(0)
		EventData_minusBG[i]=EventData[i]-BackgroundDataMean[i]
	plt.plot(xx,EventData)
	plt.plot(xx,EventData_minusBG)
	# also print vertical lines again
	for item in guards:
		plt.axvline(x=item)
	# add a relevant title	
	# plt.title(' Event # '+response+" from run# "+run_number+" and background "+background_number)
	# plt.show()
	response = raw_input("Please enter event#: ")
	
	c2 = TCanvas( 'c2', 'Event'+response+" w/ removed background", 200, 10, 700, 500 )
	c2.SetFillColor( 42 )
	c2.SetGrid()
	
	n=len(SignalDataMean_minusBG)
	x = array ('f', xx)
	y1 = array('f', EventData)
	y2 = array('f', EventData_minusBG)

	# We need to learn how to re-configure the y'y axis with the "SAME" parameter.
	gr2 = TGraph( n, x, y1 )
	gr3 = TGraph( n, x, y2 )
	gr2.SetLineColor( 2 )
	gr2.SetLineWidth( 1 )
	gr2.SetMarkerColor( 1 )
	gr2.SetMarkerStyle( 11 )
	gr2.GetYaxis().SetTitle( 'Y title' )
	gr3.GetXaxis().SetTitle( 'X title' )
	gr3.GetYaxis().SetTitle( 'Y title' )

	gr2.Draw( )
	gr2.SetTitle("Event"+response+" w/ removed background")
	gr3.Draw( 'SAME')        
	c2.SetGrid()
	c2.GetFrame().SetFillColor( 21 )
	c2.GetFrame().SetBorderSize( 12 )
	c2.Modified()
	c2.Update()
	



if response == "0":
	print "Section 2 - Finished\n\n"
	print "We start the analysis after this point \n \n \n"	

# #Section 3


# t = time.time()
# # do stuff
# print time.time() - t	


Area1rms = FetchDataPoints(Eventrun, "extra", "Area1rms_BG18")
Area2mean = FetchDataPoints(Eventrun, "extra", "Area2mean_BG18")
Area4mean = FetchDataPoints(Eventrun, "extra", "Area4mean_BG18")
SACharge = FetchDataPoints(Eventrun, "extra", "SignalArea_Charge_BG18")
SA_Pulse = FetchDataPoints(Eventrun, "extra", "SignalArea_PulseHeight_BG18")
SA_Peak = FetchDataPoints(Eventrun, "extra", "SignalArea_PeakDistr_BG18")

#===========================================================================================================
# # Create a new canvas, and customize it.
c5 = TCanvas( 'c5', 'histo1', 200, 10, 700, 500 )
c5.SetFillColor( 0 )
c5.GetFrame().SetFillColor( 10 )
c5.GetFrame().SetBorderSize( 6 )
c5.GetFrame().SetBorderMode( -1 )

histo1 = TH1F( 'Charge_25-18', 'SignalArea_Charge_BG18', 100, 0.05, 2)
for item in SACharge:
	histo1.Fill(item)
	
histo1.Fit("gaus")
histo1.GetMean()

histo1.Draw()
c5.Modified()
c5.Update()
raw_input("Press Enter to continue... \n \n ")
#===========================================================================================================

#===========================================================================================================
c6 = TCanvas( 'c6', 'histo2', 200, 10, 700, 500 )
c6.SetFillColor( 0 )
c6.GetFrame().SetFillColor( 10 )
c6.GetFrame().SetBorderSize( 6 )
c6.GetFrame().SetBorderMode( -1 )

histo2 = TH1F( 'PeakDistribution_25-18', 'SignalArea_PeakDistr_BG18', 500, 0.0, 500)
for item in SA_Peak:
	histo2.Fill(item)

histo2.Fit("gaus")
histo2.GetMean()

histo2.Draw()
c6.Modified()
c6.Update()
raw_input("Press Enter to continue... \n \n")
#===========================================================================================================

#===========================================================================================================
c7 = TCanvas( 'c7', 'histo3', 200, 10, 700, 500 )
c7.SetFillColor( 0 )
c7.GetFrame().SetFillColor( 10 )
c7.GetFrame().SetBorderSize( 6 )
c7.GetFrame().SetBorderMode( -1 )

histo3 = TH1F( 'PulseHeight_25-18', 'SignalArea_PulseHeight_BG18', 100, -0.05, 0.001)
for item in SA_Pulse:
	histo3.Fill(item)

histo3.Fit("gaus")
histo3.GetMean()
# # print "-->", gaus.GetParameter(0)
# # print "-->", gaus.GetParameter(1)
# # print "-->", gaus.GetParameter(2)

histo3.Draw()
c7.Modified()
c7.Update()
raw_input("Press Enter to continue... \n \n ")
#===========================================================================================================

# NTuple_io = TNtuple ( 'conceptNTuple2', 'conceptNTuple3', 'a:b:cc')
# Branch_io = Treefile.Branch( 'conceptBranch5', InputArray1, 'conceptbranch5/D')

# for i in xrange(500-2):
	# InputArray1[0] = list[i]													# because it only fills the first fuckin value, we change the first value only
	# NTuple_io.Fill(InputArray2[i], 1, InputArray2[i]*1000)
	# Treefile.Fill()

# tree1=ROOTfile.Get('conceptTree') 
# i=0
# for event in tree1:
	# print type(event)
	# print type(event.conceptBranch5)
	# print event.conceptBranch5													# for item in tree : print event.leaf

# ntup = ROOTfile.Get('conceptNTuple2')
# i=0
# for event in ntup:
	# # print event.b
	# # print type(event)																<class '__main__.TNtuple'>
	# # print type(event.cc)															<type 'float'>
	# i+=1
# print "i = ", i

# Create a histogram
# Taken from example
# histo1    = TH1F( 'Title?', 'This is an example HistograM', 100, 0.00001, 2)
# for event in ntup:
	# histo1.Fill(event.a)
		
# print "---> ", histo1.GetMean()
# print "---> ", histo1.GetRMS()
# histo1.Fit('gaus')
# print "---> ", gaus.GetParameter(0)
# print "---> ", gaus.GetParameter(1)
# print "---> ", gaus.GetParameter(2)

# Do we have to have same-sized branches on our trees? wth man.	smh


	

    



# f = TBrowser()



#========================================================================
#=========	by Tsilias Paschalis (AUTh)	=================================
#========================================================================
#===	Section.80	=====================================================
#========================================================================
#========================================================================
#========================================================================

raw_input("Press Enter to continue...")
print "Done"
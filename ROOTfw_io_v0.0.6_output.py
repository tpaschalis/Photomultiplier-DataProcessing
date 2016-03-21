
# ToDo VERY VERY UBER IMPORTANT 
# CHANCE cname, cnameCH, cnamePH, cnamePD EVERYWHERE
# PLZ DO ASAP


import sys
import os
sys.path.append("C:\\root_v5.34.34\\bin")
from ROOT import *
import ROOT as ROOT
import imp
import time
import numpy as np
import matplotlib.pyplot as plt
import math

from datetime import datetime
# FORMAT = '%Y%m%d%H%M%S'
# FORMAT = '"%Y-%m-%d %H:%M"'
FORMAT = '%c'



from ROOT import TFile, TTree	
from array import array

# model snippet
# f = open('myfile','w')
# f.write('hi there\n')
# f.close()

q = open('GeneralOutput.txt','a')


# Variable used throughout the code
# It shouldn't ever be changed, except if we decide to 
# I don't know, change something crucial/terrible.
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
 
# Section 1
# These two lines need to be filled before we carry on.
xx=FetchDataPoints('18', 'events', '0')							# The '0' flag is predefined as the x'x axis.
Eventrun, Backrun = SelectRunBackground()						# We select the runs that provide the events and the background



SignalDataMean = FetchDataPoints(Eventrun, "stats", "mean")
BackgroundDataMean = FetchDataPoints(Backrun, "stats", "mean")
RMS_Mean = FetchDataPoints(Eventrun, "stats", "rms")
# print len(SignalDataMean)==len(BackgroundDataMean)
MeanError=[]
RMS=[]

shift_hor = raw_input("Shift our background horizontally by bins#: ")
if shift_hor!='0' or shift_hor != '':
	BackgroundDataMean=ShiftList_horizontally(BackgroundDataMean, shift_hor)

writein = str(datetime.now().strftime(FORMAT))+"    "+"Run "+Eventrun+", Background "+Backrun+", shifted by "+shift_hor+"\n"
q.write(writein)


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


# We can now plot sth like
# plt.title('All events - Mean +++ Background - Mean +++ mean w/ removed background')
# plt.title('All events - Ratio of one input vs another - Used in background checking')
# We should also define the guards-vertical lines that separate our areas.

c1 = TCanvas("c1","Mean values for Event and Background runs`",200,10,700,500);
c1.SetFillColor(42)
c1.SetGrid()
c1.GetFrame().SetFillColor(21)
c1.GetFrame().SetBorderSize(12)
n=len(SignalDataMean_minusBG)

x_errors=[]					#stupid shit to eliminate xaxis errorbars
for i in xrange(n):
	x_errors.append(0.)
x  = array( 'f', xx )
ex = array( 'f', x_errors)
y  = array( 'f', SignalDataMean_minusBG)
ey = array( 'f', RMS_Mean )

if n == len(xx):
	print "\n \nWe're good to go"
# we have removed the errorbar plot, and opted for two different ones
# first one would be the mean event and mean background
# second one would be their diffrerence
# we leave the code here just in case
# create the TGraphErrors and draw it
	# gr = TGraphErrors(n,x,y, ex, ey)
	
	y1 = array('f', SignalDataMean)
	y2 = array('f', SignalDataMean_minusBG)
	y3 = array('f', BackgroundDataMean)
	
	gr2 = TGraph( n, x, y1 )
	# gr3 = TGraph( n, x, y2 )
	gr4 = TGraph( n, x, y3 )
	gr2.SetTitle("Mean Event values, w/ rms errorbars.")
	gr2.SetMarkerColor(4)
	gr2.SetMarkerStyle(5)			# check Google for specific markers - this one is slim blue crosses.
	gr2.Draw("ALP")
	gr4.Draw("SAME")
	c1.Update()
	raw_input("Mean Event values with background removed.. ")
	gr3 = TGraph( n, x, y2 )
	gr3.Draw("ALP")

sumdiff=0
for i in xrange(len(y2)):
	sumdiff = sumdiff + y2[i]
print "Sum of points in plot :", sumdiff
sumdiff = None
del sumdiff

print "Section 1 - Finished"

# Section 2 
# We select a -specific- event and have its points plotted, along with the removed background
print "\n \nSection 2 - Started"

response = raw_input("Please enter event#: ")
while response!="0" and response!="":
	EventData=[]
	# fetch 500 data for this event only
	EventData = FetchDataPoints(Eventrun, 'events', str(response))
	EventData_minusBG=[]
	for i in xrange(points_per_event):
		EventData_minusBG.append(0)
		EventData_minusBG[i]=EventData[i]-BackgroundDataMean[i]
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
	



if response == "0" or response == "":
	print "Section 2 - Finished\n\n"
	print "We start our data analysis after this point \n \n \n"	

# #Section 3

# t = time.time()
# # do stuff
# print time.time() - t	

#Maybe use 'exec' expression, as these are pretty coherent.
Area1rms = FetchDataPoints(Eventrun, "extra", "Area1rms_BG18")
Area1mean = FetchDataPoints(Eventrun, "extra", "Area1mean_BG18")
Area2mean = FetchDataPoints(Eventrun, "extra", "Area2mean_BG18")
Area2rms = FetchDataPoints(Eventrun, "extra", "Area2rms_BG18")
Area4mean = FetchDataPoints(Eventrun, "extra", "Area4mean_BG18")
Area4rms = FetchDataPoints(Eventrun, "extra", "Area4rms_BG18")
Area5mean = FetchDataPoints(Eventrun, "extra", "Area5mean_BG18")
Area5rms = FetchDataPoints(Eventrun, "extra", "Area5rms_BG18")
SACharge = FetchDataPoints(Eventrun, "extra", "SignalArea_Charge_BG18")
SA_Pulse = FetchDataPoints(Eventrun, "extra", "SignalArea_PulseHeight_BG18")
SA_Peak = FetchDataPoints(Eventrun, "extra", "SignalArea_PeakDistr_BG18")

#===========================================================================================================
#===========================================================================================================
#===========================================================================================================
c10 = TCanvas( 'c10', 'histo1', 200, 10, 700, 500 )
c10.SetFillColor( 0 )
c10.GetFrame().SetFillColor( 10 )
c10.GetFrame().SetBorderSize( 6 )
c10.GetFrame().SetBorderMode( -1 )

cname = 'A1Mean_'+"Run"+Eventrun+'-BG18'+"Sh"+str(shift_hor)+".root"
histo1 = TH1F( cname, cname, 100,-0.001,0.001)
for item in Area1mean:
	histo1.Fill(item)
	
histo1.Fit("gaus")
correction1 = gaus.GetParameter(1)
histo1.Draw()
c10.Modified()
c10.Update()
c10.Print(cname)
writein = "Baseline offset for Area1 - The mean of the Area1 fit, is "+str(correction1)
print writein
q.write(writein+"\n")
raw_input("Press Enter to continue... \n \n ")



#===========================================================================================================
#===========================================================================================================
#===========================================================================================================
c10 = TCanvas( 'c10', 'histo1', 200, 10, 700, 500 )
c10.SetFillColor( 0 )
c10.GetFrame().SetFillColor( 10 )
c10.GetFrame().SetBorderSize( 6 )
c10.GetFrame().SetBorderMode( -1 )

cname = 'A1rms_'+"Run"+Eventrun+'-BG18'+"Sh"+str(shift_hor)+".root"
histo1 = TH1F(cname, cname, 100,0.,0.001)
for item in Area1rms:
	histo1.Fill(item)
	
histo1.Fit("gaus")
histo1.GetMean()

histo1.Draw()
c10.Modified()
c10.Update()
c10.Print(cname)
raw_input("Press Enter to continue... \n \n ")



#===========================================================================================================
#===========================================================================================================
#===========================================================================================================

c10 = TCanvas( 'c10', 'histo1', 200, 10, 700, 500 )
c10.SetFillColor( 0 )
c10.GetFrame().SetFillColor( 10 )
c10.GetFrame().SetBorderSize( 6 )
c10.GetFrame().SetBorderMode( -1 )

cname = 'A2Mean_'+"Run"+Eventrun+'-BG18'+"Sh"+str(shift_hor)+".root"
histo1 = TH1F(cname,cname, 100,-0.001,0.001)
for item in Area2mean:
	histo1.Fill(item)
	
histo1.Fit("gaus")
correction2 = gaus.GetParameter(1)

histo1.Draw()
c10.Modified()
c10.Update()
c10.Print(cname)

writein = "Baseline offset for Area2 - The mean of the Area2 fit, is "+str(correction2)
print writein
q.write(writein+"\n")
correction = (correction1+correction2)/2

writein= "The mean correction in Area1 and Area2 is "+str(correction)
print writein
q.write(writein+"\n")

# We use these baseline offsets to re-calibrate the Charge fits.
CorrectionCharge = -(guards[3]-guards[2])*0.2*correction*1000/50
# print CorrectionCharge

raw_input("Press Enter to continue... \n \n ")


#===========================================================================================================
#===========================================================================================================
#===========================================================================================================
c10 = TCanvas( 'c10', 'histo1', 200, 10, 700, 500 )
c10.SetFillColor( 0 )
c10.GetFrame().SetFillColor( 10 )
c10.GetFrame().SetBorderSize( 6 )
c10.GetFrame().SetBorderMode( -1 )

cname = 'A2rms_'+"Run"+Eventrun+'-BG18'+"Sh"+str(shift_hor)+".root"
histo1 = TH1F(cname, cname, 100,0.,0.003)
for item in Area2rms:
	histo1.Fill(item)
	
histo1.Fit("gaus")
histo1.GetMean()

histo1.Draw()
c10.Modified()
c10.Update()
c10.Print(cname)
raw_input("Press Enter to continue... \n \n ")

#===========================================================================================================
#===========================================================================================================
#===========================================================================================================

c5 = TCanvas( 'c5', 'histo1', 200, 10, 700, 500 )
c5.SetFillColor( 0 )
c5.GetFrame().SetFillColor( 10 )
c5.GetFrame().SetBorderSize( 6 )
c5.GetFrame().SetBorderMode( -1 )

cnameCharge = 'SignalArea_Charge_'+"Run"+Eventrun+'-BG18'+"Sh"+str(shift_hor)+".root"
histo1 = TH1F(cnameCharge , cnameCharge, 50, 0., 2.)
for item in SACharge:
	histo1.Fill(item)

g1= TF1('g1', 'gaus', 0.1,2.)
histo1.Fit(g1, "R")
a= g1.GetParameter(0)
b= g1.GetParameter(1)
c= g1.GetParameter(2)
# print "a,b,c", a,b,c
histo1.GetMean()

g2 = TF1('g2', "exp([0]+[1]*x) + [2]*exp(-0.5*((x-[3])/[4])^2)", 0., 2.)
g2.FixParameter(2,a)
g2.FixParameter(3,b)
g2.FixParameter(4,c)
histo1.Fit(g2)

g3 = TF1('g3', "exp([0]+[1]*x) + [2]*exp(-0.5*((x-[3])/[4])^2)", 0., 2.)
g3.SetParameter(0,g2.GetParameter(0))
g3.SetParameter(1,g2.GetParameter(1))
g3.SetParameter(2,g2.GetParameter(2))
g3.SetParameter(3,g2.GetParameter(3))
g3.SetParameter(4,g2.GetParameter(4))
histo1.Fit(g3)


histo1.Draw()

ChargeMean = g3.GetParameter(3) - CorrectionCharge
ChargeSigma = g3.GetParameter(4)
print "\nThe charge correction value is,", CorrectionCharge
print "The corrected Charge mean value is ", ChargeMean, "with a sigma value of", ChargeSigma
print "and estimation errors", g3.GetParError(3), "\n"

writein =  "\nThe charge correction value is "+str(CorrectionCharge)+"\nThe corrected Charge mean value is "+str(ChargeMean)+" with a sigma value of "+str(ChargeSigma)+" and estimation errors "+str(g3.GetParError(3))
q.write(writein+"\n")
#We use this 'recalibrated' charge, from the offsets of Areas 1 and 2.


# print "=========================		Polya fit	================================================"
# polyafit1  = TF1 ( "polyafit1", "[0]*ROOT::Math::negative_binomial_pdf([1],x,[2])", 0.08, 2.)
# histo1.Fit(polyafit1, "R")
# print "=========================		Polya fit	================================================"

histo1.Draw()
c5.Modified()
c5.Update()
c5.Print(cnameCharge)
raw_input("Press Enter to continue... \n \n ")
#===========================================================================================================
#===========================================================================================================
#===========================================================================================================

c6 = TCanvas( 'c6', 'histo2', 200, 10, 700, 500 )
c6.SetFillColor( 0 )
c6.GetFrame().SetFillColor( 10 )
c6.GetFrame().SetBorderSize( 6 )
c6.GetFrame().SetBorderMode( -1 )

cnamePD = 'SignalArea_PeakDistr_'+"Run"+Eventrun+'-BG18'+"Sh"+str(shift_hor)+".root"
histo2 = TH1F(cnamePD, cnamePD, 500, 0.0, 500)
for item in SA_Peak:
	histo2.Fill(item)

histo2.Fit("gaus")
histo2.GetMean()

histo2.Draw()
c6.Modified()
c6.Update()
c6.Print(cnamePD)
raw_input("Press Enter to continue... \n \n")

#===========================================================================================================
#===========================================================================================================
#===========================================================================================================
c7 = TCanvas( 'c7', 'histo3', 200, 10, 700, 500 )
c7.SetFillColor( 0 )
c7.GetFrame().SetFillColor( 10 )
c7.GetFrame().SetBorderSize( 6 )
c7.GetFrame().SetBorderMode( -1 )

cnamePH = 'SignalArea_PulseHeight_'+"Run"+Eventrun+'-BG18'+"Sh"+str(shift_hor)+".root"
histo3 = TH1F( cnamePH,cnamePH, 50, -0.05, 0.)
for item in SA_Pulse:
	histo3.Fill(item)

g4= TF1('g4', 'gaus', -0.05,-0.008)
histo3.Fit(g4, "R")

a= g4.GetParameter(0)
b= g4.GetParameter(1)
c= g4.GetParameter(2)
# print "a,b,c", a,b,c

g5=TF1('g5', "[0]*exp(-0.5*((x-[1])/[2])^2) + [3]*exp(-0.5*((x-[4])/[5])^2)", -0.05, 0.)
g5.FixParameter(3,a)
g5.FixParameter(4,b)
g5.FixParameter(5,c)
g5.SetParameter(0,5000)
g5.SetParameter(1,-0.001)
g5.SetParameter(2,0.001)
histo3.Fit(g5)

g6=TF1('g6', "[0]*exp(-0.5*((x-[1])/[2])^2) + [3]*exp(-0.5*((x-[4])/[5])^2)", -0.05, 0.)
g6.SetParameter(0,g5.GetParameter(0))
g6.SetParameter(1,g5.GetParameter(1))
g6.SetParameter(2,g5.GetParameter(2))
g6.SetParameter(3,g5.GetParameter(3))
g6.SetParameter(4,g5.GetParameter(4))
g6.SetParameter(5,g5.GetParameter(5))
histo3.Fit(g6)


# print "=========================		Polya fit	================================================"
# polyafit2  = TF1 ( "polyafit2", "[0]*ROOT::Math::negative_binomial_pdf(x,[1],[2])", -0.005, 0.)
# polyafit3  = TF1 ( "polyafit2", "[0]*TMath::Gamma(x+[1])/(TMath::Gamma(x+1)*TMath:: Gamma([1]))*(TMath::Power(([2]/([2]+[1])),x))*(TMath::Power(([1]/([2]+[1])) ,[1]))", -0.005, 0.)
# polyafit2.SetParameter(0,1.e6)
# polyafit2.SetParameter(1,10)
# polyafit2.SetParameter(2,500.)
# histo3.Fit(polyafit2, "R")
# print "\n		-		\n"
# histo3.Fit(polyafit3, "R")
# print "=========================		Polya fit	================================================"

histo3.Draw()

CorrectedPV = g6.GetParameter(4)-correction
sigmaPV = g6.GetParameter(5)
print "\n Corrected PulseHeight is", CorrectedPV, "with a sigma of", sigmaPV
print "and estimation errors", g3.GetParError(4), "\n"

writein= "Corrected PulseHeight is "+str(CorrectedPV)+" with a sigma of "+str(sigmaPV)+" and estimation errors "+str(g3.GetParError(4))
q.write(writein+"\n")

c7.Modified()
c7.Update()
c7.Print(cnamePH)
raw_input("Press Enter to continue... \n \n ")

#===========================================================================================================
#===========================================================================================================
#===========================================================================================================
c10 = TCanvas( 'c10', 'histo1', 200, 10, 700, 500 )
c10.SetFillColor( 0 )
c10.GetFrame().SetFillColor( 10 )
c10.GetFrame().SetBorderSize( 6 )
c10.GetFrame().SetBorderMode( -1 )

cname = 'A4Mean_'+"Run"+Eventrun+'-BG18'+"Sh"+str(shift_hor)+".root"
histo1 = TH1F( cname,cname , 100,-0.001,0.001)
for item in Area4mean:
	histo1.Fill(item)
	
histo1.Fit("gaus")
histo1.GetMean()

histo1.Draw()

c10.Modified()
c10.Update()
c10.Print(cname)
raw_input("Press Enter to continue... \n \n ")



#===========================================================================================================
#===========================================================================================================
#===========================================================================================================
c10 = TCanvas( 'c10', 'histo1', 200, 10, 700, 500 )
c10.SetFillColor( 0 )
c10.GetFrame().SetFillColor( 10 )
c10.GetFrame().SetBorderSize( 6 )
c10.GetFrame().SetBorderMode( -1 )
cname = 'A4rms_'+"Run"+Eventrun+'-BG18'+"Sh"+str(shift_hor)+".root"
histo1 = TH1F(cname,cname, 100,0.,0.001)
for item in Area4rms:
	histo1.Fill(item)
	
histo1.Fit("gaus")
histo1.GetMean()

histo1.Draw()

c10.Modified()
c10.Update()
c10.Print(cname)
raw_input("Press Enter to continue... \n \n ")

#===========================================================================================================
#===========================================================================================================
#===========================================================================================================
c10 = TCanvas( 'c10', 'histo1', 200, 10, 700, 500 )
c10.SetFillColor( 0 )
c10.GetFrame().SetFillColor( 10 )
c10.GetFrame().SetBorderSize( 6 )
c10.GetFrame().SetBorderMode( -1 )

cname = 'A5Mean_'+"Run"+Eventrun+'-BG18'+"Sh"+str(shift_hor)+".root"
histo1 = TH1F( cname,cname, 100,-0.001,0.001)
for item in Area5mean:
	histo1.Fill(item)
	
histo1.Fit("gaus")
histo1.GetMean()

histo1.Draw()
c10.Modified()
c10.Update()
c10.Print(cname)
raw_input("Press Enter to continue... \n \n ")


#===========================================================================================================
#===========================================================================================================
#===========================================================================================================
c10 = TCanvas( 'c10', 'histo1', 200, 10, 700, 500 )
c10.SetFillColor( 0 )
c10.GetFrame().SetFillColor( 10 )
c10.GetFrame().SetBorderSize( 6 )
c10.GetFrame().SetBorderMode( -1 )

cname = 'A5rms_'+"Run"+Eventrun+'-BG18'+"Sh"+str(shift_hor)+".root"

histo1 = TH1F( cname,cname , 100,0.,0.001)
for item in Area5rms:
	histo1.Fill(item)
	
histo1.Fit("gaus")
histo1.GetMean()

histo1.Draw()
c10.Modified()
c10.Update()
c10.Print(cname)
raw_input("Press Enter to continue... \n \n ")

q.write("\n\n\n")
q.close()


f = TBrowser()
def ROOTexamples():
	# NTuple_io = TNtuple ( 'conceptNTuple2', 'conceptNTuple3', 'a:b:cc')
	# Branch_io = Treefile.Branch( 'conceptBranch5', InputArray1, 'conceptbranch5/D')

	# Fill tree, and ntuple w/ 3 subarrays
	# for i in xrange(500-2):
		# InputArray1[0] = list[i]													# because it only fills the first fuckin value, we change the first value only
		# NTuple_io.Fill(InputArray2[i], 1, InputArray2[i]*1000)
		# Treefile.Fill()

	# tree1=ROOTfile.Get('conceptTree') 
	# for event in tree1:
		# print type(event)
		# print type(event.conceptBranch5)
		# print event.conceptBranch5													# for item in tree : print event.leaf

	# ntup = ROOTfile.Get('conceptNTuple2')
	# for event in ntup:
		# # print event.b
		# # print type(event)																<class '__main__.TNtuple'>
		# # print type(event.cc)															<type 'float'>

	# Fill histogram from tree/leaf
	# histo1    = TH1F( 'Title?', 'This is an example HistograM', 100, 0.00001, 2)
	# for event in ntup:
		# histo1.Fill(event.a)
	pass








#========================================================================
#=========	by Tsilias Paschalis (AUTh)	=================================
#========================================================================
#===	Section.80	=====================================================
#========================================================================
#========================================================================
#========================================================================

raw_input("Press Enter to continue...")
print "Done"
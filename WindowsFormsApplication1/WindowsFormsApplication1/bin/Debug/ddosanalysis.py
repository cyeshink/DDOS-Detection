#using linux log file
import sys
yearoffset = 0
prevmonth = ""
helpfulfile = open("helpfulfile.txt", 'w')
for arg in sys.argv:
	filename = arg
inputfile = open(filename, 'r')
outputfilename = filename[0:filename.find(".log")]
outputfilename += ".daf"
print(outputfilename)
outputfile = open(outputfilename, 'w')

inputlines = inputfile.readlines()
if len(inputlines) == 0:
	print("Error: Empty file!")
	System.exit(0)

IPs = {}
linenum = 1

for line in inputlines:
	linelist = line.split()
	date = "Month, Date: " + ', '.join(linelist[0:2])
	time = "Time: " + linelist[2]
	srcpt = ""
	dstpt = ""
	proto = ""
	for ll in linelist:
		if ll.find("SPT") != -1:
			srcpt = ll.replace("SPT=", "Source Port: ")
		elif ll.find("DPT") != -1:
			dstpt = ll.replace("DPT=", "Destination Port: ")
		elif ll.find("PROTO") != -1:
			proto = ll.replace("PROTO", "Protocol: ")
	srcip = linelist[7].replace("SRC=", "Source IP: ")
	dstip = linelist[8].replace("DST=", "Destination IP: ")



	if(srcip not in IPs):
		IPs[srcip] = [[srcpt, date, time, dstip, proto, dstpt]]
	else:
		IPs[srcip].append([srcpt, date, time, dstip, proto, dstpt])
	linenum += 1

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
daysinmonths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
usedmonths = [0]*12
def findindex(item):
	#print("findindex called with " + item)
	for i in range(len(months)):
		#print(item + " = " + months[i] + "?")
		if item.find(months[i]) != -1:
			#print("Month = " + item + " = " + str(i))
			return i
	return 11


def calculatetime(entry):
	global prevmonth
	global yearoffset
	date = entry[1].split(":")[1].split(",")
	time1 = entry[2].split(":")
	hour = time1[1]
	minute = time1[2]
	second = time1[3]
	month = date[0]
	day = date[1]
	time2 = 0
	if findindex(month) < findindex(prevmonth):
		yearoffset += 365
	for days in daysinmonths[0:findindex(month)]:
		time2 += days
	time2 += int(day)
	time2 += int(hour)/24.0
	time2 += int(minute)/(24.0*60)
	time2 += int(second)/(24.0*60*60)
	time2 += yearoffset
	prevmonth = month
	return time2

IPsTimes = {}
for ip in IPs:
	prevmonth = ""
	yearoffset = 0
	entries = IPs[ip]
	if len(entries) < 50:
		continue
	times = []
	for entry in entries:
		t = calculatetime(entry)
		#print("time = " + str(t) + " for entry " + str(entry))
		times.append(t)
	times.sort()
	avgfrequency = len(entries)/(times[-1] - times[0])#attempts per day
	if avgfrequency > 100000:
		outputfile.write("0 " + str(ip) + "\n" + str(len(entries)) + "\n")
		for entry in entries:
			if entry[4].find(ip) == -1:
				outputfile.write("1 " + "\t" + str(";                 ".join(entry)) + "\n")
			#else:#for debugging purposes
				#print("\t" + str(";                 ".join(entry)) + "\n")









inputfile.close()
outputfile.close()
helpfulfile.close()
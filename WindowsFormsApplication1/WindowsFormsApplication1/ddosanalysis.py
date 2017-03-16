#using linux log file
import sys

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

IPs = {}
linenum = 1

for line in inputlines:
	linelist = line.split()
	#if len(linelist) < 17:
	#	print(str(linenum) + "\n" + str(line) + "\n" + str(inputlines[linenum+1]) + "\n")
	date = linelist[0:2]
	time = linelist[2]
	srcpt = ""
	dstpt = ""
	proto = ""
	for ll in linelist:
		if ll.find("SPT") != -1:
			srcpt = ll
		elif ll.find("DPT") != -1:
			dstpt = ll
		elif ll.find("PROTO") != -1:
			proto = ll
	srcip = linelist[7]
	dstip = linelist[8]

	if(srcip not in IPs):
		IPs[srcip] = [[srcpt, date, time, dstip, proto, dstpt]]
	else:
		IPs[srcip].append([srcpt, date, time, dstip, proto, dstpt])
	linenum += 1

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
daysinmonths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
def calculatetime(entry):
	date = entry[1]
	
	time1 = entry[2].split(":")
	hour = time1[0]
	minute = time1[1]
	second = time1[2]
	month = date[0]
	day = date[1]
	#time2 is time in days
	time2 = 0
	#time2 = sum([days[1] for days in daysinmonth[0:(daysinmonth.index(month))])
	for days in daysinmonths[0:months.index(month)]:
		time2 += days
	time2 += int(day)
	time2 += int(hour)/24.0
	time2 += int(minute)/(24.0*60)
	time2 += int(second)/(24.0*60*60)
	return time2

#outputfile.write(str(IPs))
IPsTimes = {}
for ip in IPs:
	entries = IPs[ip]
	if len(entries) < 50:
		continue
	times = []
	for entry in entries:
		t = calculatetime(entry)
		#print("time for entry " + str(entry) + " = " + str(t))
		times.append(t)
	#print(times[0])
	#print(times[-1])
	avgfrequency = len(entries)/(times[0] - times[-1])#attempts per day
	if avgfrequency > 1000:
		outputfile.write("0 " + str(ip) + "\n" + str(len(entries)) + "\n")
		for entry in entries:
			outputfile.write("1 " + "\t" + str(entry) + "\n")









inputfile.close()
outputfile.close()
helpfulfile.close()
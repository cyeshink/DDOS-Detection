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
def findindex(l, item):
	for i in range(len(l)):
		if l[i].find(item) != -1:
			return i

def calculatetime(entry):
	date = entry[1].split(":")[1].split(",")
	time1 = entry[2].split(":")
	hour = time1[1]
	minute = time1[2]
	second = time1[3]
	month = date[0]
	day = date[1]
	time2 = 0
	for days in daysinmonths[0:findindex(months, month)]:
		time2 += days
	time2 += int(day)
	time2 += int(hour)/24.0
	time2 += int(minute)/(24.0*60)
	time2 += int(second)/(24.0*60*60)
	return time2

IPsTimes = {}
for ip in IPs:
	entries = IPs[ip]
	if len(entries) < 50:
		continue
	times = []
	for entry in entries:
		t = calculatetime(entry)
		times.append(t)
	avgfrequency = len(entries)/(times[0] - times[-1])#attempts per day
	if avgfrequency > 5000:
		outputfile.write("0 " + str(ip) + "\n" + str(len(entries)) + "\n")
		for entry in entries:
			if entry[4].find(ip) == -1:
				outputfile.write("1 " + "\t" + str(";                 ".join(entry)) + "\n")
			else:#for debugging purposes
				print("\t" + str(";                 ".join(entry)) + "\n")









inputfile.close()
outputfile.close()
helpfulfile.close()
#using linux log file
import sys


filename = sys.argv[1]
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
	srcip = linelist[7]
	dstip = linelist[8]
	if len(linelist) > 15:
		proto = linelist[14]
	if len(linelist) > 16:
		srcpt = linelist[15]
	if len(linelist) > 17:	
		dstpt = linelist[16]

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
	times = [calculatetime(entry) for entry in entries]
	avgfrequency = len(entries)/(times[0] - times[-1])#attempts per day
	if avgfrequency > 100:
		outputfile.write(str(ip) + "\n")
		for entry in entries:
			outputfile.write("\t" + str(entry) + "\n")









inputfile.close()
outputfile.close()
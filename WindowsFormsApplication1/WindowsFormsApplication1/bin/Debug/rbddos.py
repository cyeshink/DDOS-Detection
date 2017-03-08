#!/usr/bin/env python
import sys

for arg in sys.argv:
    log = arg
file = open(arg, 'r') 
arg = arg.strip(".txt")
arg += ".daf"
daf = open(arg, 'w')
cnt = 0
prevtime = 0
userfriendlyoutput = []
detailedoutput     = []
for curlog in file.readlines():
    logn, date, time, etc, protocol, x, port, ipin, ipout = curlog.split()
    if prevtime == time:
        cnt += 1
    else:
        cnt = 0
    if cnt == 50 and previpout == ipout and ipin!=ipout:
        userfriendlyDDOSEntry = ipout#..
        detailedDDOSEntry = "Date: " + date + " \tLog#: " + str(int(logn)-cnt) + " \tTime: " + time#...
        userfriendlyoutput.append(userfriendlyDDOSEntry)
        detailedoutput.append(detailedDDOSEntry)
    prevtime = time
    previpout = ipout
for i in range(len(userfriendlyoutput)):
    print >> daf, "ddos #" + str(i+1)
    print >> daf, "IP address: " + userfriendlyoutput[i]
    print >> daf, detailedoutput[i]
	#daf.write("ddos#" + str(i+1))
	#daf.write("IP address: " + userfriendlyoutput[i])
	#daf.write(detailedoutput[i])
file.close()
daf.close()
    
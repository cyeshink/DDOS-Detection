#!/usr/bin/env python
import sys

for arg in sys.argv:
    log = arg
file = open(arg, 'r')
lines = file.readlines()
if len(lines)==0:
    print 'Incorrect Log Format or Empty Log'
    sys.exit(0)
arg = arg.strip(".txt")
arg += ".daf"
daf = open(arg, 'w')
cnt = 0
freq = 1
previpout = 0
prevtime = 0
check = 0
llist = []
userfriendlyoutput = []
detailedoutput     = []

for curlog in lines:
    if check == 0:
        llist = curlog.split(' ')
        if not llist:
            print 'Incorrect Log Format'
            sys.exit(0)
        elif len(llist) != 9:
            print 'Incorrect Log Format'
            sys.exit(0)
        else:
            check == 1
    logn, date, time, etc, protocol, x, port, ipin, ipout = curlog.split()
    if prevtime == time and previpout == ipout and ipin!=ipout:
        cnt += 1
    else:
        if prevtime != time and previpout == ipout and ipin!=ipout and cnt/freq >= 30:
            cnt += 1
            freq += 1
        else:
            if cnt >= 50:
                userfriendlyDDOSEntry = previpout + " \t# of attacks: " + str(cnt)
                detailedDDOSEntry = "Date: " + date + " \tLog#: " + str(int(logn)-cnt) + " \tTime: " + prevtime
                userfriendlyoutput.append(userfriendlyDDOSEntry)
                detailedoutput.append(detailedDDOSEntry)
            cnt = 0
    prevtime = time
    previpout = ipout
for i in range(len(userfriendlyoutput)):
    print >> daf, "ddos #" + str(i+1)
    print >> daf, "IP address: " + userfriendlyoutput[i]
    print >> daf, detailedoutput[i]
file.close()
daf.close()
    

#!/usr/bin/env python
import sys
import os

for arg in sys.argv:
    log = arg
file = open(arg, 'r')
if os.stat(log).st_size==0:
    print 'Incorrect Log Format or Empty Log'
    sys.exit(0)
daf = open('report.daf', 'w')
cnt = 0
prevtime = 0
check = 0
llist = []
userfriendlyoutput = []
detailedoutput     = []
for curlog in file.readlines():
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

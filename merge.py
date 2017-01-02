import optparse, sys, os
from collections import namedtuple

optparser = optparse.OptionParser()
optparser.add_option("-i", dest="input", help="input multiple srt files")
optparser.add_option("-o", dest="output", help="output file")
(opts, _) = optparser.parse_args()

inputfile = opts.input.strip().split(" ")

sub = namedtuple("sub", "begin, end, content")

inputcontent = []

def process(line):
    (begin, end) = line[1][:-2].strip().split(" --> ")
    content = line[2:]
    return sub(begin, end, content)

def time(rawtime):
    (hour, minute, seconds) = rawtime.strip().split(":")
    (second, milisecond) = seconds.strip().split(",")
    return int(milisecond) + 1000 * int(second) + 1000 * 60 * int(minute) + 1000 * 60 * 60 * int(hour)

def findnext(point, inputcontent):
    smallest = sys.maxint
    smallestid = 0
    for i in range(len(point)):
        if point[i] == len(inputcontent[i]):
            continue
        else:
            begintime = time(inputcontent[i][point[i]].begin) 
            if begintime < smallest:        
                smallest = begintime
                smallestid = i
    return smallestid

def merge(inputcontent):
    outputcontent = []
    point = [0 for i in inputcontent]
    maxpoint = [0 for i in inputcontent]
    for i in range(len(inputcontent)):
        maxpoint[i] = len(inputcontent[i])
    while point != maxpoint:
        nextid = findnext(point, inputcontent)
        outputcontent.append(inputcontent[nextid][point[nextid]])
        point[nextid] += 1
    return outputcontent

def printsub(raw, f):
    outputfile = open(f, 'w')
    for i in range(len(raw)):
        outputfile.write("%d\r\n" % (i+1))
        outputfile.write("%s --> %s \r\n" % (raw[i].begin, raw[i].end))
        for c in raw[i].content:
            outputfile.write("%s"%c)
        outputfile.write("\r\n")

for f in inputfile:
    line = []
    content = []
    for l in open(f):
        if l == "\r\n":
            content.append(process(line))
            line = []
        else:
            line.append(l)
    inputcontent.append(content)

outputraw = merge(inputcontent)
printsub(outputraw, opts.output)

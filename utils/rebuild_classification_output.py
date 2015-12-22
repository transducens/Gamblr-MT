import sys

target = open(sys.argv[1], "r")

countline=0

for line in target:
  line=line.strip()
  words=line.split()
  countword=0
  for w in words:
    print "OnLine-SBI\t"+str(countline)+"\t"+str(countword)+"\t"+w+"\t"+sys.stdin.readline().strip()
    countword+=1
  countline+=1
target.close()

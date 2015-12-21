import sys

previous_number="0"
newline=[]
for line in sys.stdin:
  fields=line.strip().split("\t")
  curr_number=fields[1]
  if previous_number != curr_number:
    print " ".join(newline)
    newline=[]
    newline.append(fields[4])
    previous_number=curr_number;
  else:
    newline.append(fields[4])
print " ".join(newline)

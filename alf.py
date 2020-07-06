import sys

#Prints the number in the alphabet (0-indexed) of a letter.

b=str(sys.argv[1]).lower()
a="abcdefghijklmnopqrstuvwxyz"
a=list(a)
o=[]

for c in b:
    o.append(a.index(c))

print(o)

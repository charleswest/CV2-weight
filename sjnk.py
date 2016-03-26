 
unsort = open('idGRule.py','r')

rl = unsort.readlines()
ly  = [x for x in rl  if len(x) > 20]
xkey = lambda instr: str(instr[15:18] + instr[-3:-1])
for xx in ly:
    print xkey(xx)

lines = sorted(ly   , key = lambda instr: (instr[15:18] + instr[-3:-1]) )

pl = ' ' ; c = 0
for l in lines:
    
    if l != pl:
        print l,
        pl = l
        c += 1
##    else:
##        print 'dup',l

 

print c, 'lines printed'

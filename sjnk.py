
unsort = open('idGRule.py','r')

rl = unsort.readlines()
for x in rl:
    x = x.strip()
ly  = [x for x in rl  if len(x) > 20]
xkey = lambda instr: '{}{}'.format(instr[15:18] , instr[-3:-1] ) 
#for xx in ly:
   # print xkey(xx)

lines = sorted(ly   , key = (lambda instr: '{}{}{}'.format(instr[15:18]
                                                       , instr[-3:-1].strip()
                                                       ,  instr[19:-1]  ))

                             )

pl = ' ' ; c = 0; d = 0
for l in lines:
    
    if l != pl:
        print l,
        
        c += 1
    else:
 #       print 'dup',l
        d += 1
        
    pl = l
 

print  'lines printed {} dup {}'.format(c,d)

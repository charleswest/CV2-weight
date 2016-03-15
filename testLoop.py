'''
This program loads all the images with filenames in the
file tfile sorted by wt, fat or h2o in order fully test
the program.  Problems are logged in the .TRB file that is created
on open.
'''
import time
from datetime import datetime
stime =  datetime.now()
from cwUtils import *
import numpy as np
import cv2
import warnings
from  weight import Scale,   iHunt 
 
import  os, glob
global db
db = False
tfile = r'C:\Users\charles\Desktop\ScTest\Qtest.txt'
tfile = r'C:\Users\charles\Desktop\ScTest\wtDataTst.txt'
#tfile = r'C:\Users\charles\Desktop\ScTest\Tdec30G1.txt'   #  large scTest no on Github
tfile = 'ScTest\\T2015Doris.txt'      #    should work on Git Hub with limited ScTest
#      only one tfile will run 
try:
    trb = open(tfile.replace('txt','TRB.txt'),'w')
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
    trb = open('VM-trb.txt','w')            # catch all problem file for VMs


print 'input test file ', tfile
c = [0,0,0] ; f = [0,0,0]
correct = 0; failed = 0;
def srtkey(lin):
    f = eval(lin)[1]
    fds =  f.find(r'\201')        #   will return date of file
    #print f[fds:]
    return(f[fds:])

with open(tfile,'r' ) as fr:
     
  for line in fr:
  #for line in sorted(fr, key = srtkey,reverse=True) :
      print line
      print eval(line)[1]
    
      x = eval(line)
      #   line has wt,fat,h20 , " filename"
      wfile = x[1]             #   filename 
      data = eval( x[0])
      trueWt = data[0]         #   see key above
      prob = False
      #rd  = rScale(wfile,False )
      s = Scale(wfile,db)
        
      #for i in range(0,3):
##      if data[1] <> s.nfat: raise ValueError('fat failed')
##      if data[2] <> s.nh2o: raise ValueError('h2o failed')
      for i,rd in enumerate ([s.nwt, s.nfat, s.nh2o]):
         if rd == data[i]:
            print (rd ,  '  is correct')
            correct = correct + 1
            c[i] = c[i] + 1
         else:
            failed = failed + 1
            f[i]   = f[i] + 1
            print '>>>>>>>>>>>>' ,rd, 'not equal to', data[i]
            prob = True
      total = correct + failed
      if prob: trb.write(line)
      print ('                                     ', correct ,'right out of ', total)
      pOK = correct * 100.0 / total
      lxtime = datetime.now()
      print 'lxtime', lxtime
      ex = lxtime - stime  
      print ' stime', stime
      
      ex = lxtime - stime; av = ex / total
      print 'el time avg',  str(ex)[2:10] , str(av)[2:10],('    pct OK is', round(pOK,2))
      print "================ end Testloop   ===================="
trb.close()     
cvd()
print ('****************************************************************')
t = [0,0,0]
for i in range(0,3):
     t[i] = c[i] + f[i] 
     print  ( ('wt ','fat','h20')[i] , c[i], ' ok of ' ,
               t[i], f[i],'wrong' , round( 100*c[i]/t[i],2), '%'  )
##print 'blob dict'
##
##iHunt = sorted(iHunt, key=lambda b: (b[0], b[1]))
##print 'sorted'
##ti = 0
##for i in iHunt:
##   print 'type hcnt tx  ex nn' , i
##   if i[0] <> 'xcrop':  ti = ti + i[1]      # accumulate ihunt depth
##print 'Average Depth of search' , 1.0 * ti / len(iHunt)

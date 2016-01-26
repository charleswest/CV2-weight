'''
This program loads all the images with filenames in the
file tfile sorted by wt, fat or h2o in order to derive a
list of likely spots to look at for each number
'''
import time
from datetime import datetime
stime =  datetime.now()
from SimpleCV import Display, Image, Color
from  weight import Scale, d, iHunt, Gd
 
import  os, glob
global Gd,db
#tfile = 'C:\\Users\\charles\\Desktop\\ScTest\\Qtest.txt'
#tfile = 'C:\\Users\\charles\\Desktop\\ScTest\\TX\\wtDataTst.txt'
#tfile = 'C:\\Users\\charles\\Desktop\\ScTest\\Weight\\Tdec30G1.txt'
tfile = 'ScTest\\T2015Doris.txt'      #    should work on Git Hub

trb = open(tfile.replace('txt','TRB.txt'),'w')
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
      s = Scale(wfile)
      db = True ; 
      #for i in range(0,3):
      #if data[2] <> s.nh2o: raise ValueError('h2o failed')
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
Gd.quit()
print ('****************************************************************')
t = [0,0,0]
for i in range(0,3):
     t[i] = c[i] + f[i] 
     print  ( ('wt ','fat','h20')[i] , c[i], ' ok of ' ,
               t[i], f[i],'wrong' , round( 100*c[i]/t[i],2), '%'  )
print 'blob dict'
##for k,v in sorted(d.iteritems()):
##    print k ,len(v)
##    for vi in sorted(v):
##        print vi
import pickle
with  open('dic.txt','wb') as h:        #   save dictionary for later analysis
    pickle.dump(d,h )

with open('dic.txt', 'rb') as handle:   #  and make sure we can read it 
  d = pickle.loads(handle.read())
#iHunt.append((typ, hcnt, tx, iex, nn ))
iHunt = sorted(iHunt, key=lambda b: (b[0], b[1]))
print 'sorted'
ti = 0
for i in iHunt:
   print 'type hcnt tx  ex nn' , i
   if i[0] <> 'xcrop':  ti = ti + i[1]      # accumulate ihunt depth
print 'Average Depth of search' , 1.0 * ti / len(iHunt)

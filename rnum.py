
#from SimpleCV import Image, Color, Display
from cwUtils import *
import numpy as np
import cv2
import sys
global db,Gd
Rtype = 'h2o'
#Gd  = Display((1040,410)) 
iHunt = []
db = False
d = {}                      # global dictionary of n : xy values
xtyp = ''


def hunt2(imgx,typ,hcnt):
#    imgy = imgx.adaptiveScale((1040,410))
    imgy = cv2.resize(imgx, (1040,410))
    img = imgy
    img.save(Gd)
    if db: cpause('hunt 2',Gd)
    xtyp = typ
    typex = {
     #    lim   limh    ms    mx    dz   
 'wt' : [130.0,150.0,  200,  4000,  60],    
 'h2o': [ 60.0, 80.0,  150,  4000,  60],
 'fat': [  9.0, 15.0,  100,  2000,  50]     # 400    
            }
    exlist = {
            'wt' :  [12, 14,     ],
            'h2o' : [2,  8, 12  ],
            'fat' : [12,  10   ]
              }                             #  200 5 600  3000   works h20
    txlist = {
            'wt' :  [ 160, 140   ],
            'h2o' : [ 130, 160, 140   ],  #160, 140, 205 ],
            'fat' : [ 187, 160, 205, 140   ]
             }
    lim  =  typex[typ][0]    #limt[0]
    limh =  typex[typ][1]
    ms =    typex[typ][2]
    mx =    typex[typ][3]
    dz =    typex[typ][4]
   
    img.save(Gd)
    for iex in exlist[typ]:
        if db: print '-----rdNumber    ms', ms, ' mx',  mx, img.area()
        for tx in txlist[typ]:
            hcnt = hcnt + 1
            img = imgy.binarize(tx).invert()
            img = img.erode(iex)
            img.save(Gd)
            if db: cpause( ['Erode image',iex],Gd)
            # n is the pattern, rmx the max size, rms min size
            n,rmx,rms = rdNumber(img,ex=iex, ms=ms   ,dz=dz , mx = mx ,tval=-1 )
          
            if db: print '       Hunt 1 n ', hcnt,  n     #  exit here
            nn = 0; j = -1
            n.reverse()
            #nn = 100 * n[1] + 10 * n[2] + n[3] + n[4]/10.0
            if db :
                print 'n' ,n
                cpause(['nreverse',n],Gd)
            for j, xin in  enumerate(n):
                nn = nn + xin * 10**(j-1)
            if (nn > lim) and nn < limh:
                iHunt.append((typ, hcnt, iex, tx, ms,rms, mx,rmx,  nn ))
                print 'hunt rtn' ,nn
                return(nn)
            
                
             
    print '>>>>><<<<<<<<<>>>>hunt2 ' ,typ, ' failed'
    return(0)
def hunt(imgx,typ ):
    global Gd, db ,xtyp
    
    #imgy = imgx.adaptiveScale((1040,410))
    imgy = cv2.resize(imgx, (1040,410))
    #hue = max(imgy.huePeaks())[0] +15
    hue = 160
    if db: print 'max huePeaks', hue 
    hcnt = 0
    xtyp = typ
    typex = {
                 #    lim   limh    ms     mx   dz   
             'wt' : [130.0,150.0,  500,  2100,  60],    
             'h2o': [ 60.0, 80.0,  600,  3600,  60],
             'fat': [  9.0, 15.0,  450,  3600,  50]       
            }
   
    exlist = {
            'wt' :  [8,  2  ],
            'h2o' : [5,  3  ],
            'fat' : [2,  8  ]
              }                             #  200 5 600  3000   works h20
    txlist = {
            'wt' :  [ 160, 140   ],
            'h2o' : [ 140, 200   ],  #160, 140, 205 ],
            'fat' : [ 160  ,140 ]
             }
    lim  =  typex[typ][0]    #limt[0]
    limh =  typex[typ][1]
    ms =    typex[typ][2]
    mx =    typex[typ][3]
    dz =    typex[typ][4]
    #imgy.save(Gd)
    cvs(imgy)
    for iex in exlist[typ]:
        if db: print '-----rdNumber    ms', ms, ' mx',  mx #, imgy.area()

        if db: print( ['erode image',iex])
        for tx in txlist[typ]:
            #img = imgy.binarize(tx).invert()
            #img = imgy.erode(iex)
            img = erode(imgy,iex)
            cvs(img)
            hcnt = hcnt + 1
            # n is the pattern, rmx the max size, rms min size
            n,rmx,rms = rdNumber(img,ex=iex, ms=ms   ,dz=dz , mx = mx ,tval=tx )
          
            if db: print '       Hunt 1 n ', hcnt,  n     #  exit here
            nn = 0; j = -1
            n.reverse()
            #nn = 100 * n[1] + 10 * n[2] + n[3] + n[4]/10.0
            if db :
                print 'n' ,n
                cpause(['nreverse',n],Gd)
            for j, xin in  enumerate(n):
                nn = nn + xin * 10**(j-1)
            if (nn > lim) and nn < limh:
                iHunt.append((typ, hcnt, iex, tx, ms,rms, mx,rmx,  nn ))
                print 'hunt rtn' ,nn
                return(nn)
            
                
             
    print '>>>>>>>>>>>>>>>>>hunt  ' ,typ, 'failed'
    
    return(hunt2(imgx,typ,hcnt))               
def rdNumber(img, tval=160, ex=1, ms=1.0,mx=3, dz = 60):
     
    '''
    analyse the img and pass a likely set of features to qnumb for
    interpretation
    '''
    global Gd, db, d
    fz = 0; h= 0; v = 0; tgrp = [] ;numb = []
    dx = dz     
    
    print '-----rdNumber   tval',tval,' ex',ex,'ms', ms, 'mxsize', mx 
    #  img.clearLayers()
    cvs(img)   #img.save(Gd)
    fs = img.findBlobs(threshval=tval,minsize=ms, maxsize= mx  )
    
    if (fs is  None):
        if db: print ' no features found'
        img.save(Gd)
        return ([0,0,0,0],0,0)
    else:
        fs.draw(color=Color.RED,width=5)
        img.save(Gd)
        if db: cpause(['rd img fs len is ->',len(fs)],Gd)
        fs = sorted(fs, key = lambda b: b.x)
        rmx = fs[0].area()
        rmn = fs[0].area() 
        fz = 0
        xd1 = fs[0].x 
        for ix, f   in enumerate( fs):
            if f.area() < rmn: rmn = f.area()
            if f.area() > rmx: rmx = f.area()
            xd = f.x - fz
            if xd > dx:         #   dx is parm
                img.drawRectangle(f.x - xd/2.0 , 0, 1, img.height
                                    , width = 5
                                    , color=Color.RED)
                #cpause(['-----break red rec'  , f.x, ix])
                numb.append(qnumb(tgrp,img,xd1))
                xd1 = xd
                #print 'numb is ', numb
                tgrp = []
            if db: print(['ix', ix, 'x', f.x
                          ,'w', f.width()
                          ,'h', f.height()
                          ,'xd' , xd
                          ,'area' ,f.area()]
                         )
            if f.width() < 150:                      #  filter bad blobs here
                tgrp.append(f)
                f.draw(color=Color.YELLOW,width=5)
            img.save(Gd)
            #cpause('detail',Gd)
            #if 'p' in numb: break
            fz = f.x
        numb.append(qnumb(tgrp,img,xd1))
        #print 'last numb', numb
        tpat = numb                  # filter out the P junk
        #if db: cpause(['end  1 rd',tpat],Gd)
        if len(tpat)>3:
            while tpat[-1] == 'p':
                tpat.pop()
            while( tpat[0] == 'p'):
                tpat.pop(0)
      #  if db: cpause(['end rd',tpat],Gd)
        if 'p' in tpat:
            return([0,0,0,0],rmx,rmn)     #    nfg return True zero
        else:
             
            return(tpat,rmx,rmn) # maybe good numeric value
       
         
    
def qnumb(grp,img,xd):      #   what number does this group encode??
    '''
    we count horizontal bars.   The we create an encoding of the four
    possible vertical bars upper left and right lower left and right
    An 8 has three horizontal bars and all four vertical bars for an
    encoding of 3 1 1 1 1.
    returns [ number , flag]   flag is True for good number 
    '''
    global Gd
    img = img.adaptiveScale((1040,410))
    if not len(grp) > 0:
        if db: ( 'zero len group. -- quitting')
        return(0)
    #grp= [gi for gi in grp if   width(gi.x) < 200]
    
    v=0 ;  h=0;
    miny=grp[0].y
    maxy=grp[0].y
    
    vc = [] ; xl = 0; xr = 0
    hlim = 100
    #print('vsf  -- height lim ', round(vsf,2), round (hlim,2))
    xygrp = []    #    the feature set of xy values only
    for b in grp: 
        xygrp.append((b.x,b.y))     # collect the xy values 
        #print(b.x, b.y, b.height(),b.area()) # 'h limit', round(171 * vsf,2))
        if b.height() < 2* b.width(): #  formerly hlim:
            h = h + 1
        else:
            v = v + 1
            vc.append(b)   #  collect vertical segments
        if b.y < miny:
            miny = b.y
        if b.y > maxy:
            maxy = b.y
        # compute x y w h for draw rectangle
        xr = grp[0].x           #    first x value
        yr = miny               #    smallest y value
        wr = grp[-1].x -  xr    #    last largest x value - first x
         
        hr = maxy - miny   
        xll =0; xlh=0; xrl=0; xrh = 0
    for vx in vc:         #   for each vertical segment where is it ?        
        if (vx.x < wr/2 + xr) :
            if (vx.y < hr/2 + miny):
                xll = 1
            else:
                xlh = 1
        else:
            if (vx.y < hr/2 + miny):               
                xrl = 1
            else:
                xrh = 1

    img.drawRectangle(xr,yr,wr,hr,color=Color.BLUE,width=3)
    img.save(Gd)
    #if db: cpause('qnum',Gd)
    ptrn = h * 10000 +  xll *  1000 + xlh * 100 +  xrl *  10 + xrh
      #  ptrn = [h,    xll,          xlh,         xrl,         xrh]
          #  'p' in  pattern indicates problems
          #  ptrn 110 and xd < 100 also problems?
    tpat = qptrn(ptrn)
    if  ptrn == 110 :
        if db: print '<<<<<<<<<< ??? problem pattern 110 xd is  -', xd
        if xd < 100: return 'p'
    
    #print ' type is ' ,xtyp
    dk = xtyp, tpat
    if dk not in d:       #   create the blob dictionary
        d[dk] = xygrp
    else:
        d[dk] = d[dk] + xygrp
    return(tpat)    # single digit 

def qptrn(p):   #   this is the pattern of a single digit
    ''' qptrn translates the results of the pattern analysis into
         numbers
         '''
    #  ptrn = [h, v, xll, xlh, xrl, xrh]
    ptrn = {
             110: 1,   #                #  why not 11 ?
           30110: 2,                    # 1 left cntr and 1 rt cntr
           30011: 3,
           11011: 4,
           31001: 5,
           31101: 6,
           10011: 7,
           10110: 7,  
           31111: 8,
           31011: 9,
           21111: 0
          }
    if p in ptrn:
        if db: print '>>>>>>found a ', ptrn[p] , p
        return ptrn[p]
    else:                  #  we don't seem to have a number
        if db: print   (  ['<<<<<<<qptrn - pattern problem p is ', p      ])
        #cpause(  ['ptrn'                 , p      ])           
        return 'p'

import time
 
##def cpause(txt= ' ',d = Gd ):
##     
##    d.done = False
##    print (txt , 'click to continue')
##    while d.isNotDone():
##        if d.mouseLeft:
##            d.done = True
##        if d.mouseRight:
##            #Gprb.append(Gfilename)
##            rb = (d.rightButtonDownPosition())
##            print(rb)
##            if rb[1] < 15 and rb[1] > 0:
##                 d.done = True
##                 d.quit()
##                 sys.exit(1)
##                 pass
##        time.sleep(.2) 

if  __name__ == '__main__':
    print ' rnum  module regression Test'
 #  Gd  = Display((1040,410))
    for tst in [Rtype]:      #'fat','wt', 'h2o', 
        img = cv2.imread(tst +'Test.png') 
        db = True #False  #True
        cvs(img,tst)
        #cpause('test image',Gd)
        wt  = hunt(img,tst )     
        print  'result  is', wt 
        print 'iHunt',iHunt
##    print 'blob dictionary'
##    for k, v in d.iteritems():
##        print k, v
    cvd()

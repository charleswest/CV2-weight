import numpy as np
import cv2
import sys
from findBlobs import findBlobs, stdSize
from cwUtils import *
global db 
Rtyp = ['h2o']
#Gd  = Display((1040,410)) 
iHunt = []
db = False
d = {}                      # global dictionary of n : xy values
xtyp = ''


def hunt(imgx,typ ,db):
    global xtyp
    imgy = stdSize(imgx,typ)
    hcnt = 0
    xtyp = typ
    typex = {
                 #    lim   limh    ms     mx      dz   
             'wt' : [130.0,150.0,  500,    4000,   60],    
             'h2o': [ 60.0, 80.0,  300,    1500,   35],
             'fat': [  9.0, 15.0,  500,    3000,   45]   #300      
            }
   
    exlist = {
            'wt' :  [8, 2  ],
            'h2o' : [2,  8   ],
            'fat' : [2,  7  ]
              }                             #  200 5 600  3000   works h20
    txlist = {
            'wt' :  [ 160, 140   ],
            'h2o' : [ 127   ],  #160, 140, 205 ],
            'fat' : [ 160 ]
             }
    lim  =  typex[typ][0]    #limt[0]
    limh =  typex[typ][1]
    ms =    typex[typ][2]
    mx =    typex[typ][3]
    dz =    typex[typ][4]
    #imgy.save(Gd)
    for iex in exlist[typ]:
        if db: print '-----rdNumber    ms', ms, ' mx',  mx #, imgy.area()

        if db: print( ['erode image',iex])
        for tx in txlist[typ]:
            #img = imgy.binarize(tx).invert()
            #img = imgy.erode(iex)
            img =  imgy.copy()
            cvs(db,img)
            hcnt = hcnt + 1
            # n is the pattern, rmx the max size, rms min size
            n,rmx,rms = rdNumber(img,ex=iex, ms=ms   ,dz=dz , mx = mx ,tval=tx )
          
            if db: print '       Hunt 1 n ', hcnt,  n     #  exit here
            nn = 0; j = -1
            n.reverse()
            #nn = 100 * n[1] + 10 * n[2] + n[3] + n[4]/10.0
            if db :
                print 'n' ,n
                #cpause(['nreverse',n],Gd)
            for j, xin in  enumerate(n):
                nn = nn + xin * 10**(j-1)
            if (nn > lim) and nn < limh:
                iHunt.append((typ, hcnt, iex, tx, ms,rms, mx,rmx,  nn ))
                print 'hunt rtn' ,nn
                return(nn)
            
                
             
    print '>>>>>>>>>>>>>>>>>hunt  ' ,typ, 'failed'
    return (0)                          #  eliminate hunt2 for now
    return(hunt2(imgx,typ,hcnt))
def rdNumber(img, tval=160, ex=2, ms=1.0,mx=3, dz = 60):
     
    '''
    analyse the img and pass a likely set of features to qnumb for
    interpretation
    '''
    global Gd, db, d
    fz = 0; h= 0; v = 0; tgrp = [] ;numb = []
    dx = dz     
    
    print '-----rdNumber   tval',tval,' ex',ex,'ms', ms, 'mxsize', mx 
    #  img.clearLayers()
    #cvs(db,img,'fs input')   #img.save(Gd)
    fs = findBlobs(img, ms, mx ,ex, db,tval=tval )
    if not fs:
        if db: print ' no features found'
        cvs(db,img)
        return ([0,0,0,0],0,0)
    else:
#        fs = sorted(fs, key = lambda cnt: tuple(cnt[cnt[:,:,0].argmin()][0]))
        fs = sorted(fs, key = lambda cnt:cv2.contourArea(cnt))
        #print fs 
        cv2.drawContours( img, fs, -1, (0, 0, 255), 5 )      
        cvs(db,img,t=0)   
        rmx = cv2.contourArea(fs[0])        #  left most area
        rmn = rmx         
        fz = 0
        #xd1 = fs[0].x
        xd1 = rmx
        fs = sorted(fs, key = lambda cnt: tuple(cnt[cnt[:,:,0].argmin()][0]))
        for ix, f   in enumerate( fs):
            x,y,w,h = cv2.boundingRect(f)
                       #fxy = tuple(f[f[:,:,0].argmin()][0]) #  leftmost point of f
            fx = x 
            if cv2.contourArea(f) < rmn: rmn = cv2.contourArea(f)
            if cv2.contourArea(f) > rmx: rmx = cv2.contourArea(f)
            xd = fx - fz
            if xd > dx:         #   dx is parm

                ih,iw = img.shape[:2] 
                tl = (int(fx-xd/2.0),0) ;  br = int(fx-xd/2.0),ih
               # cv2.rectangle(img,(tl),(br),(0,0,255),5)   # s/b vertical line
                cv2.line(img,(tl),(br),(0,0,255),5)
                
                #cpause(['-----break red rec'  , f.x, ix])
                numb.append(qnumb(tgrp,img,xd1))
                xd1 = xd
                #print 'numb is ', numb
                tgrp = []
                               
            if db: print(['ix', ix, 'x', x
                          ,'w',  w
                          ,'h',  h
                          ,'dx', dx
                          ,'xd' , xd
                          ,'area' ,cv2.contourArea(f)]
                         )
            
            tgrp.append(f)
            #f.draw(color=Color.YELLOW,width=5)
            cv2.drawContours( img, [f], 0, (0, 255, 255), 5 ) 
            cvs(db,img)
            #cpause('detail',Gd)
            #if 'p' in numb: break
            fz = x
        numb.append(qnumb(tgrp,img,xd1))
        print 'last numb', numb
        tpat = numb 
        if  all(i == 'p' for i in tpat):
             return([0,0,0,0],rmx,rmn)     #    nfg return True zero
        
                         # filter out the P junk
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
    #img = stdSize(img,xtyp)  #cv2.resize(img, (1040,410))
    if not len(grp) > 0:
        if db: ( 'zero len group. -- quitting')
        return(0)
    #grp= [gi for gi in grp if   width(gi.x) < 200]
    x,y,w,h = cv2.boundingRect(grp[0])
    
    if db: cvs(db,img,t=0)
    v=0 ;  h=0;
    miny=y
    maxy=y
    
    vc = [] ; xl = 0; xr = 0
    hlim = 100
    #print('vsf  -- height lim ', round(vsf,2), round (hlim,2))
    #xygrp = []    #    the feature set of xy values only
    for b in grp:
       
        bx,by,bw,bh = cv2.boundingRect(b)
        #xygrp.append((x,y))     # collect the xy values 
        #print(b.x, b.y, b.height(),b.area()) # 'h limit', round(171 * vsf,2))
        if bh   < 1.1 * bw: #  formerly hlim:
            h = h + 1
        else:
            v = v + 1
            vc.append(b)   #  collect vertical segments
            
        if by < miny:
            miny = by
        if by > maxy:
            maxy = by
        # compute x y w h for draw rectangle
        zbx,zby,zbw,zbh = cv2.boundingRect(grp[0])
        xr =zbx           #    first x value
        yr = miny               #    smallest y value
        zbx,zby,zbw,zbh = cv2.boundingRect(grp[-1])
        wr = zbx -  xr    #    last largest x value - first x
        hr = maxy - miny   
        xll =0; xlh=0; xrl=0; xrh = 0
        
    for vx in vc:         #   for each vertical segment where is it ?
        vbx,vby,vbw,vbh = cv2.boundingRect(vx)
        if (vbx < wr/2 + xr) :
            if (vby < hr/2 + miny):
                xll = 1
            else:
                xlh = 1
        else:
            if (vby < hr/2 + miny):               
                xrl = 1
            else:
                xrh = 1
                
    tl = (xr,miny) ; br = ( xr +  wr, maxy)    
    cv2.rectangle(img,(tl),(br),(255,0,0),5)   
   
    if db: cvs(db,img,t=0)  #.save(Gd)
    #if db: cpause('qnum',Gd)
    ptrn = h * 10000 +  xll *  1000 + xlh * 100 +  xrl *  10 + xrh
      #  ptrn = [h,    xll,          xlh,         xrl,         xrh]
          #  'p' in  pattern indicates problems
          #  ptrn 110 and xd < 100 also problems?
    tpat = qptrn(ptrn)
##    if  ptrn == 110 :
##        if db: print '<<<<<<<<<< ??? problem pattern 110 xd is  -', xd
##       # if xd < 100: return 'p'
    return tpat


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
 

if  __name__ == '__main__':
    print ' rnum  module regression Test'
    db = True
 #  Gd  = Display((1040,410))
    for tst in Rtyp:   #[ 'wt', 'h2o']:   #['fat']:      #['fat','wt', 'h2o']; 
        img = cv2.imread(tst +'Test.png') 
       
        #cvs(db,img )
        if db:
            cvs(db,img,t=0)
            h,w = img.shape[:2]   #   h = rows,  w = cols
            print 'h {} w{}'.format(h,w)
        wt  = hunt(img,tst,db )     
        print  'result  is', wt 
        print 'iHunt',iHunt
##    print 'blob dictionary'
##    for k, v in d.iteritems():
##        print k, v
    cvd()

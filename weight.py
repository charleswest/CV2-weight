from __future__ import with_statement

import numpy as np
import cv2
global db
from cwUtils import cvs, cvd, erode 
from sworks import Cropx, Part
from rnum import iHunt,  hunt
from rdTyp import rdTyp
from DigitStat1 import xrdTyp,idGen 

class Scale:
    global tmpf 
    name = 'Scale'
    def __init__(self,fname,db,trb):
        global tmpf
        self.img = cv2.imread(fname)
        if not fname == "input.png": cv2.imwrite("input.png",self.img)
        self.cropped = Cropx(db,self.img)    # crop image
        
        [self.wt,
         self.fat,
         self.h2o] = Part(self,self.cropped,db) # partition cropped image
    
        cv2.imwrite("fatTest.png", self.fat)
        cv2.imwrite("h2oTest.png", self.h2o)
        cv2.imwrite("wtTest.png",  self.wt)
        #  hunt for the appropriate number in each partitioned image
        if db: cvs(db,self.wt,'weight',0)  
        self.nwt =  xrdTyp(self.wt,'wt',db,trb)            
        self.nfat = xrdTyp(self.fat,'fat',db,trb)            
        self.nh2o = xrdTyp(self.h2o,'h2o',db,trb)
        #cvs(db,self.cropped,'input',0)
        return(None)
    
if  __name__ == '__main__':
    global db,trb
    db = 0

    filename = 'ScTest/T2015Doris/20150130_093919.jpg'
    filename = "input.png"
    print 'weight.py', filename
    
          
    s = Scale(filename,db,trb)
   
    print  s.name, 'wt is' ,s.nwt,'iHunt global'
    for i in iHunt:
        print i
    cvs(db,s.cropped ,'test image display',0)   #   test image display
  
    cvd()
    idGen(0,trb)   # close file and cleanup
    trb.close()
    
    

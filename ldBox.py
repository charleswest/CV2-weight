import os
import glob
import time
from datetime import datetime
from cwUtils import cvs, cvd

   
def LoadWtDbox():
    """
    This program loads the last image in the  Auto Upload directory
    and outputs the weight from the image to the R project wtData in a VM
     
    '"""
    
    print __doc__
    path = ('C:\Users\charles\Dropbox\Camera Uploads\*.jpg' )  #os.getcwd()
    tnow =  str(datetime.now())[:10]  # the system date
    rawchar = 'c'
    while (rawchar == 'c'):
        files = glob.glob(path)
        f = files[-1]                            # the last file
        print f
        #                                             expected filename
        #                                   Upload\2015-01-01\20150101_100635.jpg
        #                             \Auto Upload\YYYY-MM-DD\YYYYMMDD_HHMMSS.jpg' )
        #                                      \Camera Uploads\2015-08-21 06.10.13.jpg
        fds =  f.find(r'Uploads')   +7      
        # t =         f[fds+1:fds+11]     # \yyyy

        t =    (
                      f[fds+1:fds+11] + ' '       
                    + f[fds+12:fds+14]+ ':'      # hr :
                    + f[fds+15:fds+17]           # mm
                )   
          

        td = t[:10]                       #   just the date from above
        #td = t[3:10]
        print 'tnow {}  t  {}'.format( tnow,t)
        if td == tnow:
            from weight import Scale
            import cv2
        #    from rnum import cpause
            db = False
            sx = Scale(f,db)      #    the main function of Weight that returns the number
                               # sx is a tuple of w, fat, water
            print 'Date and Time -- Deployed 16-3-15 ' , t, 'weight', sx.nwt
        #   note the raw string below 
            f  = open( r'C:\Users\charles\data\prod\wtdata\0aaScale.r', 'a')
            
            print 'updd( {}, {},  {}, {} )'.format(t,sx.nwt,sx.nfat,sx.nh2o)
            st = str(t)
            sw = str(sx.nwt) +', '+ str(sx.nfat )+ ', ' + str(sx.nh2o)
            s = "\nupdd('" + st + "'," + sw + ")"
            f.write(s)
            s = "\ninfo()"
            f.write(s)
            f.close()

            rkey = cv2.waitKey(0)
            cvd()
            rawchar = 'Q'
        else:
            print "Not today's picture"
            rawchar = raw_input('Enter c to continue else Quit ')

if  __name__ == '__main__':
    LoadWtDbox()

 
 


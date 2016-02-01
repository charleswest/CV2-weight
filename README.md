# CV2-weight OCR for pictues of a Bathroom scale
This is a port of the Simple CV weight analysis program to Open CV 3.1
Apparently Simple CV is not being supported and CV  seems to run much much faster.


Requires. Python2.7 ,Numpy , OpenCV 3.1  --

This is a prototype for software to read common machine information using a smartphone camera. The jpg from the phone has accurate date and time and so all we need to do is upload pictures to a server and parse the picture for the numbers we are interested in.  

This project also serves to demonstrate instrumentation and regression testing. The TESTLOOP.py script reads a txt file which contains the expected output and the file-name to process. It verifys that the algorithm is returning the correct numbers for each picture and keeps track of elapsed time currently around 5 sec/per picture for Simple CV and under 2 sec for OpenCV.

The weight.py script analyses a single picture.

All of the scripts can be run independently using intermediate files that are output from a prior stage. Running testloop produces a TRB file which contains a list of all images that failed the test. TRB is in a format suitable for reinput to testloop.

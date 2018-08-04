import numpy as np
import cv2
from time import gmtime, strftime

capture = cv2.VideoCapture("People.mp4")
ret, myframe = capture.read()
frame1 = myframe.copy()
height, width, channels = frame1.shape
background = np.float32(frame1)
fgbg = cv2.BackgroundSubtractorMOG()
entry = 0
exit1 = 0
A=0
B=0
file = open("newfile.txt", "w")

if not(capture.isOpened()):
    capture.open()

while(capture.isOpened()):

    
    ret, frame = capture.read()
    frame2 = frame.copy()
    sub_frame = frame.copy()
    display = frame.copy()
    result_diff = frame.copy()
    #cv2.accumulateWeighted(frame2, background, 0.2)
    #avg_background = cv2.convertScaleAbs(background)
    #sub_frame = cv2.blur(sub_frame,(3,3))
    #cv2.absdiff(sub_frame, avg_background, result_diff)
    fgmask = fgbg.apply(frame, learningRate=0.01) 

    """ ALTERNATE METHOD
    gray = cv2.cvtColor(result_diff, cv2.COLOR_BGR2GRAY)
    ret, threshold = cv2.threshold(gray,100,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU) """

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    erosion = cv2.erode(fgmask, kernel , iterations=1)    #try changing iterations sequence of closing and opening
    dilation = cv2.dilate(erosion, kernel, iterations=1)
    opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    dummy_closing = closing.copy()

    contour, heir = cv2.findContours(dummy_closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    
    CenterX = list()
    CenterY = list()
    a = 0
    b = 0
    for i in range(0, len(contour)):
        cnt = contour[i]
        hull = cv2.convexHull(cnt, returnPoints = False)
        defects = cv2.convexityDefects(cnt, hull)
        area = cv2.contourArea(cnt)
        if area > 300:
            vertices = cv2.boundingRect(cnt)
            #cv2.drawContours(display, contour, -1, (0,255,0), 3)
            moments = cv2.moments(cnt)
            Cx = int(moments['m10']/moments['m00'])
            Cy = int(moments['m01']/moments['m00'])
            CenterX.append(Cx)
            CenterY.append(Cy)
            

        
            #to put the condition for counter here
            """if Cy==150:
                                
                test_count = test_count +1
                #print test_count
                test_count1 = test_count"""


            area = cv2.contourArea(cnt)
            point1 = (vertices[0], vertices[1])
            point2 = (vertices[0] + vertices[2], vertices[1] + vertices[3])
            cv2.rectangle(display, point1, point2, (0,255,0), 1)
            cv2.circle(display, (Cx,Cy), 1, (0,0,255), -1)
    for i in range(0, len(CenterY)):
        if CenterY[i] <= (height/2):
            a = a+1
        if CenterY[i] > (height/2):
            b = b+1

    print CenterX,CenterY
    del CenterX
    del CenterY
    if (A + B) == (a+b):
        if (a-A) < 0 and (b-B) > 0:
            entry = entry +1
            file.write("Exit:" + str(exit1) + " " +  strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "\n")
            file.write("Entry:" + str(entry) + " " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "\n")
        if (a-A) > 0 and (b-B) < 0:
            exit1 = exit1 + 1
            file.write("Exit:" + str(exit1) + " " +  strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "\n")
            file.write("Entry:" + str(entry) + " " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "\n")
            
    #cv2.resizeWindow("display", 600,500)
    cv2.line(display, (0,height/2), (width,height/2), (250,6,50), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font1 = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(display, 'Entry:', (0,20), font, 1, (0,255,255), 2)
    cv2.putText(display, str(entry), (125,22), font, 1, (255,0,255), 2)
    cv2.putText(display, 'Exit:', (0,45), font1, 1, (0,255,255), 2)
    cv2.putText(display, str(exit1), (125,47), font, 1, (255,0,255), 2)

    A = a
    B = b
    cv2.imshow("display",display)
    #cv2.imshow("resltant_difference", result_diff)
    cv2.imshow("final_binary", closing)
    cv2.imshow("Subtractor MOG", fgmask )
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


capture.release()
cv2.destroyAllWindows()
        
    
        
        

        
    
    
    
    
    
    
    

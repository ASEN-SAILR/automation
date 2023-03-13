import cv2
import numpy as np

cap=cv2.VideoCapture(0)


while(True):

    ret,frame = cap.read()
    frame = cv2.resize(frame,[640,480])
    

    cv2.imshow('frame',frame)
    

    if cv2.waitKey(1) & 0xFF == ord('q'):  
        break 


out.release()
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()

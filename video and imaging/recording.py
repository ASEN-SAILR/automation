import cv2
import numpy as np

cap=cv2.VideoCapture(2)


out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'),5, [640,480])

while(True):

    ret,frame = cap.read()
    
    out.write(frame)

    cv2.imshow('frame',frame)
    

    if cv2.waitKey(1) & 0xFF == ord('q'):  
        break 


out.release()
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()
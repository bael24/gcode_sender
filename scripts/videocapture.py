#!/usr/bin/env python

import cv2
import time

cap = cv2.VideoCapture(0)

while(True):
        # Capture frame-by-frame
        time_begin = time.time()
        ret, frame = cap.read()
        time_end = time.time()
        print("Capture duration: %f secs" % (time_end - time_begin))

        # Our operations on the frame come here
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


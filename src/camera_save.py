import cv2
 
capture = cv2.VideoCapture(0)
 
fourcc = cv2.VideoWriter_fourcc(*'XVID')
videoWriter = cv2.VideoWriter('video.avi', fourcc, 30.0, (640,480))
 
frames = 50

while (frames>0):
 
    ret, frame = capture.read()
     
    if ret:
#        cv2.imshow('video', frame)
        videoWriter.write(frame)
 
    if cv2.waitKey(1) == 27:
        break
    
    frames -= 1
    print("left frames",frames)

capture.release()
videoWriter.release()
 
cv2.destroyAllWindows()

import cv2
 
capture = cv2.VideoCapture(0)

fps = capture.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
videoWriter = cv2.VideoWriter('video.avi', fourcc, 1, (int(capture.get(3)),int(capture.get(4))))
 
frames = 10
while (frames>0):
 
    ret, frame = capture.read()

    if ret:
#        cv2.imshow('video', frame)
        videoWriter.write(frame)
 
    if cv2.waitKey(1) == 27:
        break
    frames -= 1

capture.release()
videoWriter.release()
 
cv2.destroyAllWindows()

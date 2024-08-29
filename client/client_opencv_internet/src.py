import cv2

cap = cv2.VideoCapture('http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg')
#cv2.namedWindow('live cam', cv2.WINDOW_NORMAL)

while(True):
    ret, frame = cap.read()
    print(str(frame))
    #img_resize = cv2.resize(frame, (960, 540))
    #cv2.imshow('live cam', frame)
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
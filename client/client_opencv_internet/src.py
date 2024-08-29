import cv2

cap = cv2.VideoCapture('http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg')
#cv2.namedWindow('live cam', cv2.WINDOW_NORMAL)

while(True):
    ret, frame = cap.read()
    #img_resize = cv2.resize(frame, (960, 540))
    #cv2.imshow('live cam', frame)
    print('Client getting data=' + str(frame))
    if cv2.waitKey(1) == 13:
        break

cap.release()
cv2.destroyAllWindows()
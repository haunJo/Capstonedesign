import cv2
import time
from time import localtime
from time import strftime
import os

def get_image():
    print(cv2.__version__)

    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Could not Open Camera:")
        exit(0)
    
    
    currunt_time = localtime()
    timestamp = strftime('%Y_%m_%d_%I', currunt_time)
    
    try:
        if not os.path.exists(timestamp):
            os.makedirs("data/images/"+timestamp)
    except OSError:
        print("Directory is already exists : " + timestamp)
    
    
    while True:
        ret, img = cam.read()
        if not ret:
            print( "Can't read Camera")
            break
        cv2.imshow('CCTV', img)
        if cv2.waitKey(1):
            tm = localtime()
            capturedtime = strftime('%Y_%m_%d_%I%M%S%P', tm)
            img_captured = cv2.imwrite(f'data/images/{timestamp}/{capturedtime}.jpg', img)
        if cv2.waitKey(1) == ord('q'):
            break
        
    
    
    
    # count = 0
    
    # while(video.isOpened()):
    #     ret, frame = video.read()
    #     if(int(video.get(1))% int(fps) == 0):
    #         cv2.imwrite("data/images/" + filepath[-10:-4] + f"/{filepath[-10:-4]}%0d.jpg"% count, frame)
    #         print("Saved frame number:" , str(int(video.get(1))))
    #         count += 1
    #     if(ret == False):
    #         break
    cam.release()


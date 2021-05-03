from cv2 import cv2

# haar_frontface_xml = pkg_resources.resource_filename(
# 'cv2', 'data/haarcascades/haarcascade_frontalface_default.xml')
# haar_eye_xml = pkg_resources.resource_filename(
# 'cv2', 'data/haarcascades/haarcascade_frontalface_default.xml')
# haar_smile_xml = pkg_resources.resource_filename(
# 'cv2', 'data/haarcascades/haarcascade_frontalface_default.xml')

face_cascade = cv2.CascadeClassifier('/home/youming/Documents/smile_detector/haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier('/home/youming/Documents/smile_detector/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('/home/youming/Documents/smile_detector/haarcascade_smile.xml')

def detect(gray, frame):
    face = face_cascade.detectMultiScale(gray, 1.1, 5)
    for (x_face, y_face, w_face, h_face) in face:
        cv2.rectangle(frame, (x_face, y_face), (x_face+w_face, y_face+h_face), (255, 130, 0), 2)
        ri_grayscale = gray[y_face:y_face+h_face, x_face:x_face+w_face]
        ri_color = frame[y_face:y_face+h_face, x_face:x_face+w_face] 
        smile = smile_cascade.detectMultiScale(ri_grayscale, 1.7, 20)
        for (x_smile, y_smile, w_smile, h_smile) in smile: 
            cv2.rectangle(ri_color,(x_smile, y_smile),(x_smile+w_smile, y_smile+h_smile), (20, 0, 255), 2)
    return frame 

def main():
    video_capture = cv2.VideoCapture(0)
    while True:
        # Captures video_capture frame by frame
        _, frame = video_capture.read() 

        # To capture image in monochrome                    
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  

        # calls the detect() function    
        canvas = detect(gray, frame)   

        # Displays the result on camera feed                     
        cv2.imshow('Video', canvas) 

        # The control breaks once q key is pressed                        
        if cv2.waitKey(1) & 0xff == ord('q'):               
            break

    # Release the capture once all the processing is done.
    video_capture.release()                                 
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
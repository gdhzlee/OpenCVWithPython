
import cv2
cap = cv2.VideoCapture("../../../../resources/video/2.mp4")

face_cascade = cv2.CascadeClassifier("../../cascades/haarcascade_frontalface_default.xml")

i = 1
while cap.isOpened():
    ret,frame = cap.read()


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face = face_cascade.detectMultiScale(gray, 1.3, 5)
    # 人脸数目
    count = 0
    for (x, y, w, h) in face:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
    key = cv2.waitKey(10)&0xFF
    if key == 27:
        break

    cv2.imshow("faceDetect", frame)
    # if i in [1,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290]:
    #     cv2.imwrite("C:\\Users\\Lee\\Desktop\\1\\"+ str(i)+".jpg", frame)
    # i = i + 1

cv2.destroyAllWindows()
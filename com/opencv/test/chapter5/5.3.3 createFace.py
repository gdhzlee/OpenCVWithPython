import cv2

def generate():
    face_cascade = cv2.CascadeClassifier("../../cascades/haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier("../../cascades/haarcascade_eye.xml")

    img = cv2.imread("../../../../resources/image/1.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in face:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imwrite()

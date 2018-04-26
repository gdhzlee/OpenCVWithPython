import cv2

# 将识别出来的人脸保存在库中
def generate():
    face_cascade = cv2.CascadeClassifier("../../cascades/haarcascade_frontalface_default.xml")

    img = cv2.imread("../../../../resources/image/12.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face = face_cascade.detectMultiScale(gray, 1.3, 5)
    # 人脸数目
    count = 0
    for (x, y, w, h) in face:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # 将识别出来的人脸保存在人脸库当中
        f = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
        cv2.imwrite("../../../../resources/face/%s.jpg" % str(count), f)
        count += 1

if __name__ == "__main__":
    generate()


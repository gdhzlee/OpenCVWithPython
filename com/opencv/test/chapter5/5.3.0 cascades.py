import cv2

filename = "../../../../resources/image/1.jpg"

def detect(filename):
    face_cascade = cv2.CascadeClassifier("../../cascades/haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier("../../cascades/haarcascade_eye.xml")
    img = cv2.imread(filename)
    print(img.shape)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    """
    cv2.CascadeClassifier.detectMultiScale(image[, scaleFactor[, minNeighbors[, flags[, minSize[, maxSize]]]]]) → objects
    
        image – Matrix of the type CV_8U containing an image where objects are detected.
        scaleFactor – Parameter specifying how much the image size is reduced at each image scale.
        minNeighbors – Parameter specifying how many neighbors each candidate rectangle should have to retain it.
        flags – Parameter with the same meaning for an old cascade as in the function cvHaarDetectObjects. It is not used for a new cascade.
        minSize – Minimum possible object size. Objects smaller than that are ignored.
        maxSize – Maximum possible object size. Objects larger than that are ignored.
    """
    faces = face_cascade.detectMultiScale(gray, 1.3, 1)
    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    """
    cv2.CascadeClassifier.detectMultiScale(image[, scaleFactor[, minNeighbors[, flags[, minSize[, maxSize]]]]]) → objects
    
        image – Matrix of the type CV_8U containing an image where objects are detected.
        scaleFactor – Parameter specifying how much the image size is reduced at each image scale.
        minNeighbors – Parameter specifying how many neighbors each candidate rectangle should have to retain it.
        flags – Parameter with the same meaning for an old cascade as in the function cvHaarDetectObjects. It is not used for a new cascade.
        minSize – Minimum possible object size. Objects smaller than that are ignored.
        maxSize – Maximum possible object size. Objects larger than that are ignored.
    """
    eye = eye_cascade.detectMultiScale(gray, 1.03, 1, 0, (40, 40))
    for (x, y, w, h) in eye:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.namedWindow("faces")
    cv2.imshow("faces", cv2.pyrDown(img))
    cv2.waitKey(0)

detect( filename )
from face_detection.face_detection import RetinaFace
import cv2
detector = RetinaFace()
cap = cv2.VideoCapture(0)
while True:
    _, img = cap.read()
    faces = detector(img)
    if len(faces) > 0:
        for box, landmark, score in faces:
            cv2.rectangle(img, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0,0,255), 1)
    cv2.imshow('pred',img)
    cv2.waitKey(1) 
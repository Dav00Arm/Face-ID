"""LICENSE DZYADZ DAVO
ov vekalav knexanam"""

import face_recognition 
import cv2
import numpy as np
import json

# Get a new person
def canotanal():
    name = input('Your name: ')
    cap = cv2.VideoCapture(0)
    current_person = []
    i=0
    while True:
        _, frame = cap.read()
        if i % 10 == 0:
            if len(face_recognition.face_encodings(frame))>0:
                current_person.append(face_recognition.face_encodings(frame)[0])
        if i == 120:
            break
        i+=1

        cv2.imshow('img', frame)
        cv2.waitKey(1)

    with open('people.json') as json_file:
        new_person = json.load(json_file)

    new_person[name] = list(np.mean(current_person, axis=0))

    with open('people.json', 'w') as json_file:
        json.dump(new_person, json_file)

# Recognize a person
# canotanal ()


with open('people.json', 'r') as json_file:
    data = json.load(json_file)
    data_keys = list(data.keys())
    cap = cv2.VideoCapture(0)
    faces = []
    for data_key in data_keys:
        faces.append([data[data_key]])
    while True:
        _, test = cap.read()
        cpy = test.copy()
        if len(face_recognition.face_locations(test))>0:
            for i, face in enumerate(face_recognition.face_locations(test)):
                y2, x2, y1, x1 = face
                if len(face_recognition.face_encodings(test))>0:
                    test_encode = face_recognition.face_encodings(test)[i] # cpy[y1:y2, x1:x2]
                    compare = face_recognition.compare_faces(faces,test_encode[0])

                cv2.putText(cpy, data_keys[np.where(faces)[0][0]], (x1, y2+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                cv2.rectangle(cpy, (x1,y1), (x2,y2), (255,0,0), 1)
        cv2.imshow('face', cpy)
        cv2.waitKey(1)


        # test = face_recognition.load_image_file('image.jpg')
        # print(len(face_recognition.face_locations(test)))
        # test_encode = face_recognition.face_encodings(test)
        # recognized = ''
        # if len(test_encode) > 0:
        #     for data_key in data_keys:
        #             if face_recognition.compare_faces([data[data_key]],test_encode[0])[0]:
        #                 recognized = data_key
        #                 break

        # cpy = test.copy()
        # if len(face_recognition.face_locations(test))>0:
        #     if recognized != '':
        #         y2, x2, y1, x1 = face_recognition.face_locations(test)[0]
        #         cv2.rectangle(cpy, (x1,y1), (x2,y2), (255,0,0), 1)
        #         cv2.putText(cpy, recognized, (x1, y2+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        #     else:
        #         y2, x2, y1, x1 = face_recognition.face_locations(test)[0]
        #         cv2.rectangle(cpy, (x1,y1), (x2,y2), (255,0,0), 1)
        #         cv2.putText(cpy, 'unknown', (x1, y2+10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1)

        # cv2.imshow('face', cpy)
        # cv2.waitKey(1)

import face_recognition
import cv2
import numpy as np
import os
from face_detection import face_detection
from videoCapture import *
from sendData import *
import time
import tqdm

def canotanal(source):
    name = input('Your name: ')
    if not os.path.exists(f'faces/{name}'):
        os.mkdir(f'faces/{name}')
    cap = cv2.VideoCapture(source)
    img_num = 0
    i=0

    while True:
        ret, frame = cap.read()
        if i % 30 == 0:
            if len(face_recognition.face_locations(frame))>0:
                cv2.imwrite(f'faces/{name}/{img_num}.jpg', frame)
                img_num+=1
        if img_num == 10:
            break

        i+=1
        cv2.imshow('img', frame)
        cv2.waitKey(1)

def run():
    detector = face_detection.RetinaFace()
    video_capture = cv2.VideoCapture(0)

    # image encodings 
    known_face_encodings = []

    known_face_names = sorted(os.listdir('faces'))

    for person in tqdm.tqdm(known_face_names):
        current_person = []
        for face in os.listdir(f'faces/{person}'):
            # print(face_recognition.face_encodings(cv2.imread(f'faces/{person}/{face}'))[0])
            # print(len(current_person))
            face_image = cv2.imread(f'faces/{person}/{face}')
            box_,_,_ = detector(face_image)[0]
            box = (int(box_[1]), int(box_[2]), int(box_[3]), int(box_[0]))
            current_person.append(face_recognition.face_encodings(face_image, [box])[0])
        known_face_encodings.append(np.mean(current_person, axis=0))

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        #taking an frame from an the camera
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # small_frame = frame
        # Convert the image from BGR color 
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            # face_locations = face_recognition.face_locations(rgb_small_frame)
            faces = detector(rgb_small_frame)
            face_locations = []
            for box_, landmark, score in faces:
                box = (int(box_[1]), int(box_[2]), int(box_[3]), int(box_[0]))
                face_locations.append(box)
            # face_locations = [int(i) for i in face_locations]
            # print(face_locations)
            # break
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # cv2.rectangle(frame, (top, right), (bottom, left), (0, 0, 255), 2)

            # Draw a label with a name below the face
            # cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 180, 0), 2)

        # Display the resulting image
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def run_stream():
    detector = face_detection.RetinaFace()
    video_capture = VideoCaptureThreading("https://video11.sputnik.systems/cec06d76-8cf8-44f2-b34b-b8d34f3c3590/video1.ts")
    video_capture.start()
    # image encodings 
    known_face_encodings = []
    now = time.time()
    known_face_names = sorted(os.listdir('faces'))

    for person in known_face_names:
        current_person = []
        for face in os.listdir(f'faces/{person}'):
            # print(face_recognition.face_encodings(cv2.imread(f'faces/{person}/{face}'))[0])
            # print(len(current_person))
            face_image = cv2.imread(f'faces/{person}/{face}')
            box_,_,_ = detector(face_image)[0]
            box = (int(box_[1]), int(box_[2]), int(box_[3]), int(box_[0]))
            current_person.append(face_recognition.face_encodings(face_image, [box])[0])
        known_face_encodings.append(np.mean(current_person, axis=0))

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    for frame in video_capture.generator():
        #taking an frame from an the camera
        # ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # small_frame = frame
        # Convert the image from BGR color 
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            # face_locations = face_recognition.face_locations(rgb_small_frame)
            faces = detector(rgb_small_frame)
            face_locations = []
            for box_, landmark, score in faces:
                box = (int(box_[1]), int(box_[2]), int(box_[3]), int(box_[0]))
                face_locations.append(box)
            # face_locations = [int(i) for i in face_locations]
            # print(face_locations)
            # break
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # cv2.rectangle(frame, (top, right), (bottom, left), (0, 0, 255), 2)

            # Draw a label with a name below the face
            # cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            if(name == "Areg" and time.time()-now>3): 
                post_data("https://api.sputnik.systems/api/v1/account/devices/intercoms/{f916a805-81a3-4431-8205-b80de32fefc7}/open_door", {"Person": "Davit"})
                sent = True 
                now = time.time()

            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 180, 0), 2)

        # Display the resulting image
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


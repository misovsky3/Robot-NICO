import cv2
import serial
import mediapipe as mp
import math
import numpy as np
import pyfirmata
import math
import tkinter as tk

##canvas = tk.Canvas(width = 640, height = 480)
##canvas.pack()
##clear_canvas = lambda: canvas.create_rectangle(0,0,640,480,fill="white")
##make_dot = lambda x,y: canvas.create_oval(x,y,x+10,y+10,fill = "black")

board = pyfirmata.Arduino('COM9')
motor = board.get_pin('d:2:s')
# hnedy = zem
# cerveny = napatia
# zlty = pin


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

wCam, hCam = 640, 480
cam = cv2.VideoCapture(0)
cam.set(3, wCam)
cam.set(4, hCam)

with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.8,
        min_tracking_confidence=0.8) as hands:
    # nastavenie videa + rozoznanie ruk
    while cam.isOpened():
        success, image = cam.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        # popriradovanie id k clankom
        # https://google.github.io/mediapipe/images/mobile/hand_landmarks.png
        lmList = []
        if results.multi_hand_landmarks:
            myHand = results.multi_hand_landmarks[0]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

        if len(lmList) != 0:
            x1, y1 = lmList[0][1], lmList[0][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            x3, y3 = lmList[5][1], lmList[5][2]

            ##      clear_canvas()
            ##      for i in lmList:
            ##        make_dot(i[1],i[2])
            ##      canvas.update()

            cv2.circle(image, (x1, y1), 15, (255, 255, 255))
            cv2.circle(image, (x2, y2), 15, (255, 255, 255))
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 3)
            length = math.hypot(x2 - x1, y2 - y1)





            uhol = (math.degrees(math.atan2(y1-y3,x1-x3) - math.atan2(y2-y3,x2-x3)))  #x1,y1 vypocet uhla pri
            Pos = np.interp(length, [100, 200], [0, 100])
            cv2.putText(image, str(round(uhol))+"°", (50, 60), cv2.FONT_ITALIC, 2, (0, 0, 0))
            #    0008   completely open, straight
            #    1640   90 deg towards palm
            #    4005   completely closed (when thumb is straight)
            #print(np.interp(length, [100, 200], [8, 4005]))




            motorpos = (100 - round(Pos))
            print(motorpos)
            motor.write(motorpos)


        cv2.imshow('handDetector', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cam.release()

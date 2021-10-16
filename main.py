#!/usr/bin/python
# -*- coding: utf-8 -*-

from cvzone.HandTrackingModule import HandDetector
import cv2 as cv
import time
from classes import Question, DragObject


flag = False
p = 'questions/question1/'
p2 = 'questions/question2/'
p3 = 'questions/question3/'
Question1 = Question("Ktory z podanych byl krolem polski?", [f"{p}Jagielo.png", f'{p}Mieszko_I.png', f'{p}Mieszko_I.png'], [f'{p}chrobry.png'])
Question3 = Question("Which animal carries children in belly?", [f"{p2}wieloryb.png", f'{p2}koala.png', f'{p2}lew.png'], [f'{p2}kangur.png'])
Question2 = Question("Who is responsible for fighting a fires?", [f"{p3}lekarz.png", f'{p3}adwokat.png', f'{p3}policjant.png'], [f'{p3}strazak.png'])
questions = [Question1, Question2, Question3]
Resolution = (1280, 720)
try:
    Camera = cv.VideoCapture(0)
except Exception as exc:
    quit(f'Camera not found. Error:{exc}')

Camera.set(3, Resolution[0])
Camera.set(4, Resolution[1])

myPNG = cv.imread('soccer.png', cv.IMREAD_UNCHANGED)
Maksymowicz = DragObject('maksymowicz.png', [500, 400], (300, 300))
PNG_test = DragObject('soccer.png', [500, 200])
detector = HandDetector(detectionCon=0.8)
ox, oy = 500, 200

score = 0
pTime = 0
q_c = 0
Question_curr = questions[q_c]
while True:

    success, frame = Camera.read()
    if not success:
        break

    cTime = time.time()
    fps = int(1/(cTime - pTime))
    frame = cv.flip(frame, 1)

    hands = detector.findHands(frame, flipType=False, draw=False)
    if hands:
        hand1 = hands[0]
        lmList = hand1['lmList']
        length, _ = detector.findDistance(lmList[8], lmList[12])

        if length < 42:
            cursor = lmList[8]
            s, flag = Question_curr.update(cursor, frame)
            score += s
    else:
        cv.rectangle(frame, (0, 0), (15, 15), (0, 0, 255), cv.FILLED)
    frame = Question_curr.overlay_all(frame)
    Question_curr.show_text(frame)
    cv.putText(frame, f'FPS: {fps}', (1100, 35), cv.FONT_HERSHEY_COMPLEX, 1, (200, 211, 223), thickness=1)
    cv.putText(frame, f'Score: {score}', (1100, 75), cv.FONT_HERSHEY_COMPLEX, 1, (30, 231, 14), thickness=1)
    cv.imshow('Cam 1', frame)
    cv.waitKey(1)
    if flag:
        time.sleep(1.8)
        if flag == 1:
            if q_c + 1 != len(questions):
                q_c += 1
                Question_curr = questions[q_c]
            else:
                quit()
        flag = False
    pTime = cTime


cv.destroyAllWindows()
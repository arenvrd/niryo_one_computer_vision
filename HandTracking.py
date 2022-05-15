import cv2
import mediapipe as mp
import socket
import math
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5066
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

x_list = [0] * 10
y_list = [0] * 10

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    pinky = 0
    reference = 0
    finger = 1

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                #print(id, lm)
                h, w, c = img.shape
                cx, cy, cz = int(lm.x*w), int(lm.y*h), float(lm.z)
                #print(id, cx, cy, cz)
                if id == 5:
                    x0 = cx
                    y0 = cy
                    x_list.append(x0)
                    y_list.append(y0)
                    if x_list[len(x_list)-2] + 2 < x_list[len(x_list)-1]:
                        outputx = 'Right'

                    elif x_list[len(x_list)-2] > x_list[len(x_list)-1] + 2:
                        outputx = 'Left'

                    else:
                        outputx ='None'

                    if y_list[len(y_list)-2] + 2 < y_list[len(y_list)-1]:
                        outputy = 'Down'
                    elif y_list[len(y_list)-2] > y_list[len(y_list)-1] + 2:
                        outputy = 'Up'
                    else:
                        outputy = 'None'
                    #cv2.line(img, (xvalue[len(xvalue)-2], yvalue[len(yvalue)-2]), (xvalue[len(xvalue)-1], yvalue[len(yvalue)-1]), (0, 255, 0), 3, 8)
                    #print(id, x0, y0)

                if id == 0:
                    x0 = cx
                    y0 = cy

                if id == 20:
                    #cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    x20 = cx
                    y20 = cy
                    pinky = math.sqrt((x0 - x20) ** 2 + (y0 - y20) ** 2)

                if id == 5:
                    x5 = cx
                    y5 = cy
                    reference = math.sqrt((x0 - x5) ** 2 + (y0 - y5) ** 2)*0.9

                if pinky < reference:
                    finger = 0
                else:
                    finger = 1


            #print(yvalue)
            #print(xvalue)
            print(outputx+ " " + outputy + " " + str(finger))
            #print(outputx2)
            sock.sendto(str(outputx).encode(), (UDP_IP, UDP_PORT))
            sock.sendto(str(outputy).encode(), (UDP_IP, UDP_PORT))
            sock.sendto(str(finger).encode(), (UDP_IP, UDP_PORT))
            cv2.putText(img, outputx, (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(img, outputy, (400, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 2, cv2.LINE_AA)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    else:
        outputy = "None"
        outputx = "None"

        print(outputx + " " + outputy + " " + str(finger))
        sock.sendto(str(outputx).encode(), (UDP_IP, UDP_PORT))
        sock.sendto(str(outputy).encode(), (UDP_IP, UDP_PORT))
        sock.sendto(str(finger).encode(), (UDP_IP, UDP_PORT))


    cv2.imshow('Image', img)
    cv2.waitKey(1)

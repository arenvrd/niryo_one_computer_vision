import cv2
import mediapipe as mp
import math
import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5065
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  #convert to RBG because mpHands only use RGB images
    results = hands.process(imgRGB) # processes the frame and gives back result
    fingers = [0, 0, 0, 0, 0]
    reference = 0

    if results.multi_hand_landmarks: # if there is a hand
        for handLms in results.multi_hand_landmarks: # extract information of each hand handLms = single hand
            for id, lm in enumerate(handLms.landmark): # index numbers of fingers
                #print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)   # gives back cx and cy position
                #print(id, cx, cy)
                if id == 0:
                    x0 = cx
                    y0 = cy
                    #print(id, x0, y0)
                if id == 6:
                    x6 = cx
                    y6 = cy
                    index = math.sqrt((x0 - x6) ** 2 + (y0 - y6) ** 2)*0.9
                    reference = index
                if id == 4:
                    #cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    x4 = cx
                    y4 = cy
                    thumb = math.sqrt((x0-x4)**2+(y0-y4)**2)
                    fingers[0] = thumb
                    #print(id, cx, cy, thumb, cz)
                if id == 8:
                    #cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    x8 = cx
                    y8 = cy
                    index = math.sqrt((x0-x8)**2+(y0-y8)**2)
                    fingers[1] = index
                    #print(id, cx, cy, index)
                if id == 12:
                    #cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    x12 = cx
                    y12 = cy
                    middle = math.sqrt((x0-x12)**2+(y0-y12)**2)
                    fingers[2] = middle
                    #print(id, cx, cy, middle)
                if id == 16:
                    #cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    x16 = cx
                    y16 = cy
                    ring = math.sqrt((x0-x16)**2+(y0-y16)**2)
                    fingers[3] = ring
                    #print(id, cx, cy, ring)
                if id == 20:
                    #cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    x20 = cx
                    y20 = cy
                    pinky = math.sqrt((x0-x20)**2+(y0-y20)**2)
                    fingers[4] = pinky
                    #print(id, cx, cy, pinky)
                counter = 0
                for x in fingers:
                    if x > reference:
                        counter += 1
            print(counter)
            cv2.putText(img, "number of fingers: " + str(counter), (200, 70), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), 2)
            sock.sendto((str(counter)).encode(), (UDP_IP, UDP_PORT))
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS) # drawing the hand for us with connections
            time.sleep(1)



    cv2.imshow('Image', img)
    cv2.waitKey(1)
    if cv2.waitKey(1) == ord('q'):
        break



        
import cv2
import mediapipe as mp
import pyautogui 
mp_hands=mp.solutions.hands
hands=mp_hands.Hands(max_num_hands=1)
mp_draw=mp.solutions.drawing_utils

cap=cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error opening camera")
    exit()
def is_hand_closed(landmarks):
    tips_ids=[8,12,16,20]
    closed_fingers=0
    for tip_id in tips_ids:
        if landmarks[tip_id].y<landmarks[tip_id-2].y:
            closed_fingers+=1
        return closed_fingers>=3
    
while True:
    success,img=cap.read()
    if not success:
        print("Error reading frame")
        break
    img_rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result=hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img,hand_landmarks,mp_hands.HAND_CONNECTIONS)
            if is_hand_closed(hand_landmarks.landmark):
                pyautogui.scroll(-50)
                cv2.putText(img,"Closed hand->Scrolling up",(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            else:                    
                pyautogui.scroll(-50)
                cv2.putText(img,"open hand->Scrolling down",(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.imshow('Scrolling using Gestures',img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
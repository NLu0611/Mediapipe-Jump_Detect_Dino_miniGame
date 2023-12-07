import cv2
import mediapipe as mp
import pyautogui
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)
last_y = 0
last_jump_time = time.time()
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:

    if not cap.isOpened():
        print("啟動相機錯誤")
        exit()
    
    while True:
        ret, img = cap.read()
        if not ret:
            print("畫面錯誤")
            break
        img = cv2.resize(img, (568, 320))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(img_rgb)
        try:
            noses = []
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                if idx == mp_pose.PoseLandmark.NOSE.value:
                    nose_x = int(landmark.x * img.shape[1])
                    nose_y = int(landmark.y * img.shape[0])
                    noses.append((nose_x, nose_y))
            if len(noses) > 0:
                middle_x = img.shape[1] // 2
                distances = [abs(nose_x - middle_x) for nose_x, _ in noses]
                closest_nose_index = distances.index(min(distances))
                cuqcrrent_nose = False
                for idx, (nose_x, nose_y) in enumerate(noses):
                    color = (0, 255, 0) if idx == closest_nose_index else (0, 0, 255)
                    current_nose = True if idx == closest_nose_index else False
                    cv2.circle(img, (nose_x, nose_y), 10, color, -1)
                    cv2.putText(img, f'Nose {idx+1}', (nose_x, nose_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                if current_nose:
                    if last_y - nose_y > 12 and time.time() - last_jump_time > 0.5:
                        pyautogui.press('space')
                        print("按下空白鍵")
                        last_jump_time = time.time()
                    last_y = nose_y
        except Exception as e:
            print(f"錯誤: {e}")
        
        cv2.imshow('dkriecl is sabi', img)
        if cv2.waitKey(5) == ord('q'):
            break

cap.release()
print("程式關閉")
cv2.destroyAllWindows()

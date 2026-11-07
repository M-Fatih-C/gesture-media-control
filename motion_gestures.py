import cv2
import numpy as np
import pyautogui
import time
from collections import deque

cap = cv2.VideoCapture(0)

ret, frame = cap.read()
if not ret:
    print("Kamera bulunamadi.")
    exit()
bg_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
bg_gray = cv2.GaussianBlur(bg_gray, (21, 21), 0)

x_history = deque(maxlen=10)
action_cooldown = 1.5  # saniye
pause_cooldown = 2.0   # saniye

last_action_time = 0
last_pause_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    frame_delta = cv2.absdiff(bg_gray, gray)
    thresh = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_contour = None
    largest_area = 0
    center_x = None

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 15000:
            if area > largest_area:
                largest_area = area
                largest_contour = cnt

    if largest_contour is not None:
        x, y, w, h = cv2.boundingRect(largest_contour)
        center_x = x + w // 2
        x_history.append(center_x)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    else:
        x_history.clear()

    now = time.time()

    # --- 1: Soldan sağa veya sağdan sola sallama ile şarkı geçişi ---
    if len(x_history) == x_history.maxlen:
        diff = x_history[-1] - x_history[0]
        if diff > 120 and (now - last_action_time > action_cooldown):
            cv2.putText(frame, "SONRAKI SARKI!", (60, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
            pyautogui.hotkey('ctrl', 'right')
            last_action_time = now
            x_history.clear()
        elif diff < -120 and (now - last_action_time > action_cooldown):
            cv2.putText(frame, "ONCEKI SARKI!", (60, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
            pyautogui.hotkey('ctrl', 'left')
            last_action_time = now
            x_history.clear()

    # --- 2: Sabit bekleme ile Play/Pause ---
    if len(x_history) == x_history.maxlen:
        move_amount = max(x_history) - min(x_history)
        # El hemen hemen sabit duruyorsa ve yakın geçmişte tetiklenmediyse
        if move_amount < 30 and (now - last_pause_time > pause_cooldown):
            cv2.putText(frame, "PLAY / PAUSE", (60, 140), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 0, 0), 3)
            pyautogui.press('space')
            last_pause_time = now
            x_history.clear()

    cv2.putText(frame, "El sallayin: Sag-Sol=Onceki, Sol-Sag=Sonraki, Sabit=Play/Pause", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.imshow('Hand Control Advanced', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        bg_gray = gray.copy()
        print("Arka plan sifirlandi.")

cap.release()
cv2.destroyAllWindows()

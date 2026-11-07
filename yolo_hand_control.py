import cv2
from ultralytics import YOLO
import pyautogui
import time

# 1. EL MODELİNİ YÜKLE
model = YOLO('best.pt')  # ← Buraya kendi indirdiğin modelin adını yaz!

cap = cv2.VideoCapture(0)
last_trigger = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 2. YOLO İLE TAHMİN AL
    results = model(frame)
    el_var = False

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]
            if 'hand' in label.lower():
                el_var = True
                x1, y1, x2, y2 = [int(v) for v in box.xyxy[0]]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, "EL", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    # 3. EL ALGILANIRSA KOMUT GÖNDER
    if el_var and (time.time() - last_trigger > 2):
        print("EL ALGILANDI! Spotify'da sonraki şarkı.")
        pyautogui.hotkey('ctrl', 'right')  # Komutu buradan değiştirebilirsin!
        last_trigger = time.time()

    cv2.imshow("YOLOv8 Hand Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

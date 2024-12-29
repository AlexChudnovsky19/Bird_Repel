import cv2
from picamera2 import Picamera2
from ultralytics import YOLO
import logging

logging.basicConfig(level=logging.INFO)

model = YOLO("/home/alexchudnovsky19/Documents/Bird_Detection_System/model_nano.pt")

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

logging.info("Camera started successfully. Press 'q' to quit.")

try:
    while True:

        frame = picam2.capture_array()
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = model.predict(frame_bgr, stream=False)
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy.cpu().numpy()[0])
                confidence = box.conf.item()
                class_id = int(box.cls)
                label = f"{model.names[class_id]}: {confidence * 100:.1f}%"

                cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    frame_bgr, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2
                )

                if model.names[class_id] in ["common_myna", "grey_crow", "pigeon"]:
                    import RPi.GPIO as GPIO
                    import time

                    GPIO.setmode(GPIO.BCM)
                    print("start water shoot")

                    pin = 17
                    GPIO.setup(pin, GPIO.OUT)

                    GPIO.output(pin, GPIO.LOW)
                    time.sleep(1)
                    GPIO.output(pin, GPIO.HIGH)

                    print("end water shoot")
                    GPIO.cleanup()

        cv2.imshow("Bird Tracker", frame_bgr)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    logging.error(f"Error: {e}")
finally:
    picam2.stop()
    cv2.destroyAllWindows()

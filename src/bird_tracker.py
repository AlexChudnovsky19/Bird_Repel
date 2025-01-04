import time
import logging
import cv2
from picamera2 import Picamera2
from ultralytics import YOLO
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio
import RPi.GPIO as GPIO

logging.basicConfig(level=logging.INFO)

model = YOLO("/home/alexchudnovsky19/Documents/Bird_Detection_System/model_nano.pt")

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FRAME_CENTER_X = FRAME_WIDTH // 2
FRAME_CENTER_Y = FRAME_HEIGHT // 2

logging.info("Camera started successfully. Press 'q' to quit.")

# ------------------------------------------------------------------------------
# SERVO SETUP (PAN & TILT)
# ------------------------------------------------------------------------------
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Standard frequency for servos

PAN_CHANNEL = 0
TILT_CHANNEL = 1

pan_angle = 90
tilt_angle = 90

# Servo movement boundaries
MIN_ANGLE = 0
MAX_ANGLE = 180

def angle_to_pwm(angle):
    """
    Converts a given servo angle (0-180) to PCA9685 duty cycle.
    """
    pulse_min = 1000  # microseconds
    pulse_max = 2000  # microseconds
    pulse_range = pulse_max - pulse_min
    angle_range = 180

    pulse = pulse_min + (pulse_range * angle / angle_range)
    duty_cycle = int((pulse / 1000000) * pca.frequency * 0xFFFF)
    return duty_cycle

# Initialize servos to center
pca.channels[PAN_CHANNEL].duty_cycle = angle_to_pwm(pan_angle)
pca.channels[TILT_CHANNEL].duty_cycle = angle_to_pwm(tilt_angle)

# ------------------------------------------------------------------------------
# TRACKING PARAMETERS
# ------------------------------------------------------------------------------
# The Kp values are "proportional" constants controlling how quickly the servos move.
KP_PAN = 0.05
KP_TILT = 0.05

# ------------------------------------------------------------------------------
# WATER SHOOT SETUP
# ------------------------------------------------------------------------------
WATER_SHOOT_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(WATER_SHOOT_PIN, GPIO.OUT)
GPIO.output(WATER_SHOOT_PIN, GPIO.HIGH)

def shoot_water(duration=1.0):
    logging.info("start water shoot")
    GPIO.output(WATER_SHOOT_PIN, GPIO.LOW)
    time.sleep(duration)
    GPIO.output(WATER_SHOOT_PIN, GPIO.HIGH)
    logging.info("end water shoot")

try:
    while True:
        frame = picam2.capture_array()
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        results = model.predict(frame_bgr, stream=False)

        # We'll draw bounding boxes only for valid, high-confidence detections
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy.cpu().numpy()[0])
                confidence = box.conf.item()
                class_id = int(box.cls)
                
                if model.names[class_id] in ["common_myna", "grey_crow", "pigeon"]:
                    
                    if confidence >= 0.60:
                        label = f"{model.names[class_id]}: {confidence * 100:.1f}%"
                        cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(
                            frame_bgr,
                            label,
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 0, 255),
                            2
                        )

                        # Calculate error from frame center to track
                        box_center_x = (x1 + x2) // 2
                        box_center_y = (y1 + y2) // 2
                        error_x = box_center_x - FRAME_CENTER_X
                        error_y = box_center_y - FRAME_CENTER_Y

                        # Adjust pan/tilt angles (simple P-control)
                        pan_angle -= error_x * KP_PAN
                        tilt_angle += error_y * KP_TILT

                        # Clamp angles
                        pan_angle = max(MIN_ANGLE, min(MAX_ANGLE, pan_angle))
                        tilt_angle = max(MIN_ANGLE, min(MAX_ANGLE, tilt_angle))

                        # Send angles to servos
                        pca.channels[PAN_CHANNEL].duty_cycle = angle_to_pwm(pan_angle)
                        pca.channels[TILT_CHANNEL].duty_cycle = angle_to_pwm(tilt_angle)

                        shoot_water(duration=1.0)
                    else:
                        logging.info(
                            f"low confidence {confidence*100:.1f}% < 60%. Skipping."
                        )

        cv2.imshow("Bird Tracker", frame_bgr)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    logging.info("Keyboard interrupt received. Exiting.")
except Exception as e:
    logging.error(f"Error: {e}")
finally:
    picam2.stop()
    cv2.destroyAllWindows()

    # Reset servos to center
    pca.channels[PAN_CHANNEL].duty_cycle = angle_to_pwm(90)
    pca.channels[TILT_CHANNEL].duty_cycle = angle_to_pwm(90)
    pca.deinit()

    GPIO.output(WATER_SHOOT_PIN, GPIO.HIGH)
    GPIO.cleanup()

    logging.info("Exiting")

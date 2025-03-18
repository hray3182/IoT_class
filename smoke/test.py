import time
import RPi.GPIO as GPIO
SENSOR_PIN = 38
LED_PIN = 40
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(SENSOR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)
while True:

    value = GPIO.input(SENSOR_PIN)
    print(f"gas value = {value}")
    if value < 1: #low active
        GPIO.output(LED_PIN, 1)
        print("LOW ")
        print("gas detected")
    else:
        GPIO.output(LED_PIN, 0)
        print("HIGH")
        time.sleep(0.5)
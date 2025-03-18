import time
import RPi.GPIO as GPIO
MONITOR_PIN = 35
LED_PIN = 40
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(MONITOR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

# while True:
#  signal = GPIO.input(MONITOR_PIN)
#  print(signal)
#  time.sleep(0.5)
try:
    print("Press Ctrl-C to stop program")
    while True:
        GPIO.output(LED_PIN, GPIO.input(MONITOR_PIN))
        time.sleep(0.1)
except KeyboardInterrupt:
    print("close program")
finally:
    GPIO.cleanup()
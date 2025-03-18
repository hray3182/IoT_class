import RPi.GPIO as GPIO
import time
# Pin Definitions
echo_pin = 40 # using the GPIO.BOARD mode , Echo
trig_pin = 38 # using the GPIO.BOARD mode , Trig
def setup():
    #Pin Setup
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(echo_pin, GPIO.IN)
    GPIO.setup(trig_pin, GPIO.OUT)
def set_trigger_pulse():
    GPIO.output(trig_pin, GPIO.LOW)
    time.sleep(0.000005)
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.00001) # 10us
    GPIO.output(trig_pin, GPIO.LOW)
def wait_for_echo(value, timeout):
    count = timeout
    while GPIO.input(echo_pin) == value and count > 0:
        count = count - 1
def get_distance():
    set_trigger_pulse()
    wait_for_echo(GPIO.LOW, 5000)
    start = time.time()
    wait_for_echo(GPIO.HIGH, 5000)
    finish = time.time()
    pulse_len = finish - start
    #distance_cm = pulse_len * 340 *100 /2
    v = 331+0.6*25 # v = 331+0.6*T
    distance_cm = pulse_len * v *100 /2
    return distance_cm
def main():
    setup()
    try:
        while True:
            print("cm=%f" % get_distance())
            time.sleep(1)
    except KeyboardInterrupt:
        print("close program")
    finally:
        GPIO.cleanup()
if __name__ == '__main__':
    main()
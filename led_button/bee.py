import RPi.GPIO as gpio
import time

piano = list([261, 293, 329, 349, 391, 440, 493, 523])
buzzer = 36

gpio.setmode(gpio.BCM)
gpio.setup(buzzer, gpio.OUT)


def play(pitch, sec):
    half_pitch = (1 / pitch) / 2
    t = int(pitch * sec)
    for i in range(t):
        gpio.output(buzzer, gpio.HIGH)
        time.sleep(half_pitch)
        gpio.output(buzzer, gpio.LOW)
        time.sleep(half_pitch)


for p in piano:
    play(p, 1)

gpio.cleanup()
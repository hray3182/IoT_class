import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# 設定 RGB LED 的 GPIO 腳位
red = 3
green = 5
blue = 12

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

# 使用 PWM 控制亮度，頻率設定為 100Hz
red_pwm = GPIO.PWM(red, 100)
green_pwm = GPIO.PWM(green, 100)
blue_pwm = GPIO.PWM(blue, 100)

red_pwm.start(0)
green_pwm.start(0)
blue_pwm.start(0)

def fade_in_out(pwm, delay=0.02):
    """ 讓 LED 緩慢變亮再變暗 """
    for duty in range(0, 101, 2):  # 逐漸變亮
        pwm.ChangeDutyCycle(duty)
        time.sleep(delay)
    for duty in range(100, -1, -2):  # 逐漸變暗
        pwm.ChangeDutyCycle(duty)
        time.sleep(delay)

try:
    while True:
        fade_in_out(red_pwm)   # 紅色變亮變暗
        fade_in_out(green_pwm) # 綠色變亮變暗
        fade_in_out(blue_pwm)  # 藍色變亮變暗
except KeyboardInterrupt:
    pass
finally:
    red_pwm.stop()
    green_pwm.stop()
    blue_pwm.stop()
    GPIO.cleanup()

    

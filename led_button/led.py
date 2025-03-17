import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# 設定 RGB LED 的 GPIO 腳位
red = 3
green = 5
blue = 7

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

def rainbow_breath_effect(delay=0.01):
    """ 產生七彩呼吸效果 """
    # 定義不同顏色組合 (R, G, B)
    colors = [
        (100, 0, 0),    # 紅
        (100, 50, 0),   # 橙
        (100, 100, 0),  # 黃
        (0, 100, 0),    # 綠
        (0, 0, 100),    # 藍
        (50, 0, 100),   # 靛
        (100, 0, 100)   # 紫
    ]
    
    for r, g, b in colors:
        # 逐漸變亮
        for duty in range(0, 101, 2):
            red_pwm.ChangeDutyCycle(r * duty / 100)
            green_pwm.ChangeDutyCycle(g * duty / 100)
            blue_pwm.ChangeDutyCycle(b * duty / 100)
            time.sleep(delay)
            
        time.sleep(0.2)  # 在最亮處停留一下
        
        # 逐漸變暗
        for duty in range(100, -1, -2):
            red_pwm.ChangeDutyCycle(r * duty / 100)
            green_pwm.ChangeDutyCycle(g * duty / 100)
            blue_pwm.ChangeDutyCycle(b * duty / 100)
            time.sleep(delay)

try:
    while True:
        rainbow_breath_effect()  # 顯示七彩呼吸效果
except KeyboardInterrupt:
    pass
finally:
    red_pwm.stop()
    green_pwm.stop()
    blue_pwm.stop()
    GPIO.cleanup()

    

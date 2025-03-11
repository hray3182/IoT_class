import time
import RPi.GPIO as GPIO

# 設置 GPIO 模式
GPIO.setmode(GPIO.BOARD)

# 定義 RGB LED 的 GPIO 腳位
R_pin = 33
G_pin = 35
B_pin = 37

GPIO.setup(R_pin, GPIO.OUT)
GPIO.setup(G_pin, GPIO.OUT)
GPIO.setup(B_pin, GPIO.OUT)

# PWM 頻率設定為 800Hz
R_pwm = GPIO.PWM(R_pin, 250)
G_pwm = GPIO.PWM(G_pin, 250)
B_pwm = GPIO.PWM(B_pin, 250)

R_pwm.start(100)  # 反向，100 代表關
G_pwm.start(100)
B_pwm.start(100)

# 七彩霓虹燈顏色變化 (RGB)
colors = [
    (255, 0, 0),    # 紅色
    (255, 165, 0),  # 橙色
    (255, 255, 0),  # 黃色
    (0, 255, 0),    # 綠色
    (0, 255, 255),  # 青色
    (0, 0, 255),    # 藍色
    (255, 0, 255)   # 紫色
]

def smooth_transition(start_color, end_color, steps=100, delay=0.02):
    """ 讓 LED 漸變顏色，並反轉 PWM 輸出 """
    R1, G1, B1 = start_color
    R2, G2, B2 = end_color

    for i in range(steps):
        R = int(R1 + (R2 - R1) * (i / steps))
        G = int(G1 + (G2 - G1) * (i / steps))
        B = int(B1 + (B2 - B1) * (i / steps))

        # 反轉 PWM 設定 (0=開, 255=關)
        R_pwm.ChangeDutyCycle(100 - (R / 255 * 100))
        G_pwm.ChangeDutyCycle(100 - (G / 255 * 100))
        B_pwm.ChangeDutyCycle(100 - (B / 255 * 100))

        time.sleep(delay)

try:
    while True:
        for i in range(len(colors)):
            start_color = colors[i]
            end_color = colors[(i + 1) % len(colors)]  # 循環到下一個顏色
            smooth_transition(start_color, end_color)

except KeyboardInterrupt:
    pass
finally:
    R_pwm.stop()
    G_pwm.stop()
    B_pwm.stop()
    GPIO.cleanup()

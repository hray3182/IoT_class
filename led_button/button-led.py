import RPi.GPIO as GPIO
import time

# 設置 GPIO 模式為 BOARD
GPIO.setmode(GPIO.BOARD)

# 定義 RGB LED 的 GPIO 腳位
R_pin = 33
G_pin = 35
B_pin = 37
button_pin = 36  # 假設按鈕接在物理引腳 36

GPIO.setup(R_pin, GPIO.OUT)
GPIO.setup(G_pin, GPIO.OUT)
GPIO.setup(B_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # 使用內建的下拉電阻

# PWM 頻率設定為 250Hz
R_pwm = GPIO.PWM(R_pin, 250)
G_pwm = GPIO.PWM(G_pin, 250)
B_pwm = GPIO.PWM(B_pin, 250)

R_pwm.start(0)  # 初始化為關閉 (0% duty cycle)
G_pwm.start(0)
B_pwm.start(0)

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

        # 設定 PWM duty cycle (0-100)
        R_pwm.ChangeDutyCycle(R / 255 * 100)
        G_pwm.ChangeDutyCycle(G / 255 * 100)
        B_pwm.ChangeDutyCycle(B / 255 * 100)

        time.sleep(delay)

def toggle_led(on):
    """ 控制 LED 開關 """
    if on:
        for i in range(len(colors)):
            start_color = colors[i]
            end_color = colors[(i + 1) % len(colors)]  # 循環到下一個顏色
            smooth_transition(start_color, end_color)
    else:
        R_pwm.ChangeDutyCycle(0)  # 關閉紅色
        G_pwm.ChangeDutyCycle(0)  # 關閉綠色
        B_pwm.ChangeDutyCycle(0)  # 關閉藍色

# 全域變數
led_on = False

# 設定回調函數以監聽引腳狀態變化
def pin36_callback(channel):
    global led_on
    time.sleep(0.05)  # 反彈跳延遲
    if GPIO.input(36) == GPIO.HIGH:  # 確認按鈕狀態 (避免彈跳)
        print("Pin 36 is HIGH (Button Pressed or Input Active)")
        led_on = not led_on  # 切換 LED 狀態
        toggle_led(led_on)  # 根據狀態控制 LED
    else:
        print("Pin 36 is LOW (Button Released or Input Inactive)")

# 設定事件檢測，當引腳 36 狀態改變時觸發回調函數
GPIO.add_event_detect(36, GPIO.BOTH, callback=pin36_callback)

try:
    print("Monitoring pin 36...")
    while True:
        time.sleep(1)  # 程式持續運行直到被中斷
except KeyboardInterrupt:
    print("Program interrupted")
finally:
    R_pwm.stop()
    G_pwm.stop()
    B_pwm.stop()
    GPIO.cleanup()  # 清理 GPIO 設定
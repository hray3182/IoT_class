import time
import RPi.GPIO as GPIO

# 設定 GPIO 模式
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# 設定 RGB LED 的 GPIO 腳位
RED_PIN = 3
GREEN_PIN = 5
BLUE_PIN = 7

# 設定 GPIO 輸出
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

# 使用 PWM 控制亮度，頻率設定為 100Hz
red_pwm = GPIO.PWM(RED_PIN, 100)
green_pwm = GPIO.PWM(GREEN_PIN, 100)
blue_pwm = GPIO.PWM(BLUE_PIN, 100)

# 啟動 PWM，初始值為 0（LED 關閉）
red_pwm.start(0)
green_pwm.start(0)
blue_pwm.start(0)

def set_color(r, g, b):
    """設定 RGB LED 的顏色
    
    參數:
        r (int): 紅色亮度 (0-100)
        g (int): 綠色亮度 (0-100)
        b (int): 藍色亮度 (0-100)
    """
    red_pwm.ChangeDutyCycle(r)
    green_pwm.ChangeDutyCycle(g)
    blue_pwm.ChangeDutyCycle(b)

def test_basic_colors():
    """測試基本顏色"""
    print("測試基本顏色...")
    
    # 紅色
    print("紅色")
    set_color(100, 0, 0)
    time.sleep(1)
    
    # 綠色
    print("綠色")
    set_color(0, 100, 0)
    time.sleep(1)
    
    # 藍色
    print("藍色")
    set_color(0, 0, 100)
    time.sleep(1)
    
    # 黃色 (紅 + 綠)
    print("黃色")
    set_color(100, 100, 0)
    time.sleep(1)
    
    # 紫色 (紅 + 藍)
    print("紫色")
    set_color(100, 0, 100)
    time.sleep(1)
    
    # 青色 (綠 + 藍)
    print("青色")
    set_color(0, 100, 100)
    time.sleep(1)
    
    # 白色 (紅 + 綠 + 藍)
    print("白色")
    set_color(100, 100, 100)
    time.sleep(1)
    
    # 關閉
    set_color(0, 0, 0)

def color_fade(delay=0.02):
    """顏色漸變效果"""
    print("顏色漸變效果...")
    
    # 紅色漸變
    print("紅色漸變")
    for duty in range(0, 101, 2):
        set_color(duty, 0, 0)
        time.sleep(delay)
    for duty in range(100, -1, -2):
        set_color(duty, 0, 0)
        time.sleep(delay)
    
    # 綠色漸變
    print("綠色漸變")
    for duty in range(0, 101, 2):
        set_color(0, duty, 0)
        time.sleep(delay)
    for duty in range(100, -1, -2):
        set_color(0, duty, 0)
        time.sleep(delay)
    
    # 藍色漸變
    print("藍色漸變")
    for duty in range(0, 101, 2):
        set_color(0, 0, duty)
        time.sleep(delay)
    for duty in range(100, -1, -2):
        set_color(0, 0, duty)
        time.sleep(delay)

def rainbow_cycle(cycles=3, delay=0.01):
    """彩虹循環效果"""
    print("彩虹循環效果...")
    
    # 定義彩虹顏色序列 (R, G, B)
    colors = [
        (100, 0, 0),    # 紅
        (100, 50, 0),   # 橙
        (100, 100, 0),  # 黃
        (0, 100, 0),    # 綠
        (0, 100, 100),  # 青
        (0, 0, 100),    # 藍
        (100, 0, 100)   # 紫
    ]
    
    for _ in range(cycles):
        for r, g, b in colors:
            set_color(r, g, b)
            time.sleep(0.5)

try:
    print("開始 RGB LED 測試...")
    
    # 測試基本顏色
    test_basic_colors()
    time.sleep(1)
    
    # 測試顏色漸變
    color_fade()
    time.sleep(1)
    
    # 測試彩虹循環
    rainbow_cycle()
    
    print("測試完成！")

except KeyboardInterrupt:
    print("\n程式已被使用者中斷")
finally:
    # 清理資源
    red_pwm.stop()
    green_pwm.stop()
    blue_pwm.stop()
    GPIO.cleanup()
    print("GPIO 已清理")

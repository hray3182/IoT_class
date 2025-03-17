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
    """設定 RGB LED 的顏色（反轉邏輯：0=全亮，100=全暗）
    
    參數:
        r (int): 紅色亮度 (0-100，0=全亮，100=全暗)
        g (int): 綠色亮度 (0-100，0=全亮，100=全暗)
        b (int): 藍色亮度 (0-100，0=全亮，100=全暗)
    """
    red_pwm.ChangeDutyCycle(100 - r)
    green_pwm.ChangeDutyCycle(100 - g)
    blue_pwm.ChangeDutyCycle(100 - b)

def test_rgb_colors():
    """測試紅綠藍三種基本顏色（反轉邏輯）"""
    print("開始測試 RGB 三種基本顏色...")
    
    # 關閉所有顏色（在反轉邏輯中是設為100）
    print("關閉所有顏色")
    set_color(100, 100, 100)
    time.sleep(1)
    
    # 測試紅色（在反轉邏輯中是設為0,100,100）
    print("測試紅色")
    set_color(0, 100, 100)
    time.sleep(3)
    
    # 關閉所有顏色
    print("關閉所有顏色")
    set_color(100, 100, 100)
    time.sleep(1)
    
    # 測試綠色（在反轉邏輯中是設為100,0,100）
    print("測試綠色")
    set_color(100, 0, 100)
    time.sleep(3)
    
    # 關閉所有顏色
    print("關閉所有顏色")
    set_color(100, 100, 100)
    time.sleep(1)
    
    # 測試藍色（在反轉邏輯中是設為100,100,0）
    print("測試藍色")
    set_color(100, 100, 0)
    time.sleep(3)
    
    # 關閉所有顏色
    print("關閉所有顏色")
    set_color(100, 100, 100)

try:
    # 測試紅綠藍三種基本顏色
    test_rgb_colors()
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

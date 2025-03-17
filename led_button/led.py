import time
import RPi.GPIO as GPIO

# 設定 GPIO 模式
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# 設定 RGB LED 的 GPIO 腳位
RED_PIN = 3
GREEN_PIN = 5
BLUE_PIN = 11

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

def fade_in_out(pwm, delay=0.02):
    """讓 LED 緩慢變亮再變暗"""
    # 逐漸變亮
    for duty in range(0, 101, 2):
        pwm.ChangeDutyCycle(duty)
        time.sleep(delay)
    # 逐漸變暗
    for duty in range(100, -1, -2):
        pwm.ChangeDutyCycle(duty)
        time.sleep(delay)

def rainbow_breath_effect(delay=0.05):
    """產生七彩平滑過渡效果"""
    # 定義不同顏色組合 (R, G, B)，使用標準邏輯 0=全暗，100=全亮
    # set_color 函數會負責將這些值反轉為硬體所需的值
    colors = [
        (100, 0, 0),    # 紅
        (100, 50, 0),   # 橙
        (100, 100, 0),  # 黃
        (0, 100, 0),    # 綠
        (0, 0, 100),    # 藍
        (50, 0, 100),   # 靛
        (100, 0, 100)   # 紫
    ]
    
    # 設置初始顏色（從第一個顏色開始）
    current_r, current_g, current_b = colors[0]
    set_color(current_r, current_g, current_b)
    time.sleep(1)  # 在第一個顏色停留一秒
    
    # 在顏色之間平滑過渡
    for i in range(len(colors)):
        # 獲取當前顏色和下一個顏色
        current_color = colors[i]
        next_color = colors[(i + 1) % len(colors)]  # 循環到第一個顏色
        
        # 解包顏色值
        current_r, current_g, current_b = current_color
        next_r, next_g, next_b = next_color
        
        # 計算顏色差異
        diff_r = next_r - current_r
        diff_g = next_g - current_g
        diff_b = next_b - current_b
        
        # 平滑過渡到下一個顏色（50步）
        steps = 50
        for step in range(steps + 1):
            # 計算當前步驟的顏色
            ratio = step / steps
            r = current_r + diff_r * ratio
            g = current_g + diff_g * ratio
            b = current_b + diff_b * ratio
            
            # 設置顏色
            set_color(r, g, b)
            time.sleep(delay)
        
        # 在每個顏色停留一下
        time.sleep(0.5)

def main():
    """主程式"""
    try:
        print("七彩呼吸燈效果啟動")
        print("按下 Ctrl+C 可停止程式")
        
        while True:
            rainbow_breath_effect()
            
    except KeyboardInterrupt:
        print("\n程式已被使用者中斷")
    finally:
        # 清理資源
        red_pwm.stop()
        green_pwm.stop()
        blue_pwm.stop()
        GPIO.cleanup()
        print("GPIO 已清理")

# 當直接執行此檔案時執行主程式
if __name__ == "__main__":
    main()

    

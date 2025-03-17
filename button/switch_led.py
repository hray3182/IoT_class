import RPi.GPIO as GPIO
import time

# 設定 GPIO 模式
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# 設定按鈕的 GPIO 腳位
BUTTON_PIN = 13  # 按鈕連接到物理位置 13

# 設定 RGB LED 的 GPIO 腳位
RED_PIN = 3
GREEN_PIN = 5
BLUE_PIN = 11

# 設定 GPIO 輸入和輸出
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

# 使用 PWM 控制亮度，頻率設定為 1000Hz
red_pwm = GPIO.PWM(RED_PIN, 1000)
green_pwm = GPIO.PWM(GREEN_PIN, 1000)
blue_pwm = GPIO.PWM(BLUE_PIN, 1000)

# 啟動 PWM，初始值為 0（LED 關閉）
red_pwm.start(0)
green_pwm.start(0)
blue_pwm.start(0)

# 定義不同顏色組合 (R, G, B)，使用標準邏輯 0=全暗，100=全亮
colors = [
    (100, 0, 0),    # 紅
    (100, 50, 0),   # 橙
    (100, 100, 0),  # 黃
    (0, 100, 0),    # 綠
    (0, 0, 100),    # 藍
    (50, 0, 100),   # 靛
    (100, 0, 100)   # 紫
]

# 當前顏色索引
current_color_index = 0

def set_color(r, g, b):
    """設定 RGB LED 的顏色（反轉邏輯：0=全亮，100=全暗）
    
    參數:
        r (int): 紅色亮度 (0-100，0=全亮，100=全暗)
        g (int): 綠色亮度 (0-100，0=全亮，100=全暗)
        b (int): 藍色亮度 (0-100，0=全亮，100=全暗)
    """
    print(f"設置顏色: R:{r}, G:{g}, B:{b}")
    red_pwm.ChangeDutyCycle(100 - r)
    green_pwm.ChangeDutyCycle(100 - g)
    blue_pwm.ChangeDutyCycle(100 - b)

def button_callback(channel):
    """按鈕回調函數，當按鈕按下時切換顏色"""
    global current_color_index
    
    # 獲取按鈕狀態
    button_state = GPIO.input(BUTTON_PIN)
    print(f"按鈕事件觸發: 狀態 = {button_state} ({'HIGH' if button_state else 'LOW'})")
    
    # 只在按鈕按下時（LOW）切換顏色，忽略按鈕釋放（HIGH）
    if not button_state:
        # 切換到下一個顏色
        current_color_index = (current_color_index + 1) % len(colors)
        r, g, b = colors[current_color_index]
        
        # 設置新顏色
        set_color(r, g, b)
        
        # 顯示當前顏色信息
        color_names = ["紅色", "橙色", "黃色", "綠色", "藍色", "靛色", "紫色"]
        print(f"切換到顏色 {current_color_index + 1}: {color_names[current_color_index]} (R:{r}, G:{g}, B:{b})")

def main():
    """主程式"""
    global current_color_index
    
    try:
        print("RGB LED 顏色切換程式啟動")
        print(f"按鈕連接到物理位置 {BUTTON_PIN}")
        print(f"LED 連接到物理位置 紅:{RED_PIN}, 綠:{GREEN_PIN}, 藍:{BLUE_PIN}")
        print("按下按鈕切換顏色")
        print("按下 Ctrl+C 可停止程式")
        
        # 測試按鈕初始狀態
        initial_button_state = GPIO.input(BUTTON_PIN)
        print(f"按鈕初始狀態: {initial_button_state} ({'HIGH' if initial_button_state else 'LOW'})")
        
        # 設置初始顏色（第一個顏色）
        r, g, b = colors[current_color_index]
        set_color(r, g, b)
        print(f"初始顏色: 紅色 (R:{r}, G:{g}, B:{b})")
        
        # 使用輪詢方式檢測按鈕狀態，而不是事件檢測
        last_button_state = initial_button_state
        
        # 保持程式運行
        while True:
            # 讀取當前按鈕狀態
            current_button_state = GPIO.input(BUTTON_PIN)
            
            # 檢測按鈕狀態變化（從HIGH到LOW，表示按下按鈕）
            if last_button_state == 1 and current_button_state == 0:
                print("按鈕被按下")
                # 切換到下一個顏色
                current_color_index = (current_color_index + 1) % len(colors)
                r, g, b = colors[current_color_index]
                
                # 設置新顏色
                set_color(r, g, b)
                
                # 顯示當前顏色信息
                color_names = ["紅色", "橙色", "黃色", "綠色", "藍色", "靛色", "紫色"]
                print(f"切換到顏色 {current_color_index + 1}: {color_names[current_color_index]}")
            
            # 更新上一個按鈕狀態
            last_button_state = current_button_state
            
            # 短暫延遲，避免CPU使用率過高
            time.sleep(0.1)
            
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
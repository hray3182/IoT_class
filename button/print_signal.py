import RPi.GPIO as GPIO
import time

# 設定 GPIO 模式
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# 設定按鈕的 GPIO 腳位
BUTTON_PIN = 13  # 按鈕連接到物理位置 13

# 設定 GPIO 輸入，啟用內部上拉電阻
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_callback(channel):
    """按鈕回調函數，當按鈕狀態改變時調用"""
    input_value = GPIO.input(BUTTON_PIN)
    if input_value:
        print(f"按鈕釋放 (HIGH) - 輸入值: {input_value}")
    else:
        print(f"按鈕按下 (LOW) - 輸入值: {input_value}")

def main():
    """主程式"""
    try:
        print(f"按鈕監聽程式啟動，監聽物理位置 {BUTTON_PIN}")
        print("按下 Ctrl+C 可停止程式")
        
        # 添加事件檢測，當按鈕狀態改變時調用回調函數
        GPIO.add_event_detect(BUTTON_PIN, GPIO.BOTH, callback=button_callback, bouncetime=200)
        
        # 保持程式運行，並持續顯示當前輸入狀態
        while True:
            current_value = GPIO.input(BUTTON_PIN)
            print(f"當前按鈕狀態: {current_value} ({'HIGH' if current_value else 'LOW'})")
            time.sleep(1)  # 每秒更新一次
            
    except KeyboardInterrupt:
        print("\n程式已被使用者中斷")
    finally:
        # 清理資源
        GPIO.cleanup()
        print("GPIO 已清理")

# 當直接執行此檔案時執行主程式
if __name__ == "__main__":
    main()

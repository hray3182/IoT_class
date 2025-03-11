import RPi.GPIO as GPIO
import time

# 設置 GPIO 模式為 BOARD
GPIO.setmode(GPIO.BOARD)

# 設定物理引腳 36 為輸入模式
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # 使用內建的下拉電阻

# 設定回調函數以監聽引腳狀態變化
def pin36_callback(channel):
    input_state = GPIO.input(36)  # 讀取引腳 36 的輸入狀態
    if input_state == GPIO.HIGH:
        print("Pin 36 is HIGH (Button Pressed or Input Active)")
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
    GPIO.cleanup()  # 清理 GPIO 設定

import RPi.GPIO as GPIO
import time
import threading
import colorsys

# Import 各個物件
from UltrasonicSensor import UltrasonicSensor
from RgbLed import RgbLed
from Button import Button
from LedController import LedController

def main():
    """主程式"""
    # 腳位定義
    BUTTON_PIN = 3
    RED_PIN = 11
    GREEN_PIN = 13
    BLUE_PIN = 15
    TRIG_PIN = 16
    ECHO_PIN = 18
    
    # 創建控制器
    controller = LedController(
        button_pin=BUTTON_PIN,
        red_pin=RED_PIN,
        green_pin=GREEN_PIN,
        blue_pin=BLUE_PIN,
        trig_pin=TRIG_PIN,
        echo_pin=ECHO_PIN
    )
    
    try:
        # 啟動控制器
        controller.start()
        
        # 主執行緒等待，直到被中斷
        while True:
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n程式已被使用者中斷")
    finally:
        # 停止控制器
        controller.stop()


if __name__ == "__main__":
    main()
import threading
import time
import RPi.GPIO as GPIO

# Import 必要的物件
from Button import Button
from RgbLed import RgbLed
from UltrasonicSensor import UltrasonicSensor

class LedController:
    """RGB LED 控制系統，使用按鈕和距離感應器"""
    
    def __init__(self, button_pin, red_pin, green_pin, blue_pin, trig_pin, echo_pin):
        """初始化 LED 控制系統
        
        參數:
            button_pin (int): 按鈕腳位
            red_pin (int): 紅色 LED 腳位
            green_pin (int): 綠色 LED 腳位
            blue_pin (int): 藍色 LED 腳位
            trig_pin (int): 超音波感應器觸發腳位
            echo_pin (int): 超音波感應器回應腳位
        """
        # 設定 GPIO 模式
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        
        # 創建設備物件
        self.button = Button(button_pin)
        self.led = RgbLed(red_pin, green_pin, blue_pin)
        self.sensor = UltrasonicSensor(trig_pin, echo_pin)
        
        # 共享變數 - 需要在執行緒間共享的資訊
        self.hue = 0.0          # 色相 (0.0-1.0)
        self.saturation = 1.0   # 彩度 (0.0-1.0)
        self.value = 1.0        # 亮度 (0.0-1.0)
        self.running = True     # 控制程式運行
        
        # 距離參數設定
        self.min_distance = 5    # 最小距離 (cm)，低於此值視為最近
        self.max_distance = 100  # 最大距離 (cm)，超過此值視為最遠
        
        # 執行緒鎖，保護共享變數存取
        self.lock = threading.Lock()
        
        # 創建執行緒
        self.threads = []
    
    def button_thread_function(self):
        """按鈕控制執行緒，監控按鈕按下並切換色相"""
        while self.running:
            # 檢測按鈕按下
            if self.button.is_pressed():
                with self.lock:
                    # 每次按鈕按下，色相增加0.125 (45度)，形成8種基本色相
                    self.hue = (self.hue + 0.125) % 1.0
                    print(f"按鈕按下 - 新色相: {self.hue:.3f}")
            
            time.sleep(0.1)
    
    def distance_thread_function(self):
        """距離感測執行緒，根據測量距離調整彩度和亮度"""
        while self.running:
            try:
                # 測量距離
                distance = self.sensor.get_distance()
                
                # 如果距離無效或太遠，設為最大距離
                if distance < 0 or distance > self.max_distance:
                    distance = self.max_distance
                    
                # 避免距離過小
                if distance < self.min_distance:
                    distance = self.min_distance
                    
                with self.lock:
                    # 彩度計算 (越近越高)
                    # 從 MIN_DISTANCE (滿彩度) 到 MAX_DISTANCE (低彩度)
                    self.saturation = 1.0 - (distance - self.min_distance) / (self.max_distance - self.min_distance) * 0.6
                    if self.saturation < 0.4:  # 彩度最小保持0.4
                        self.saturation = 0.4
                        
                    # 亮度計算 (越近越亮)
                    # 從 MIN_DISTANCE (滿亮度) 到 MAX_DISTANCE (低亮度)
                    self.value = 1.0 - (distance - self.min_distance) / (self.max_distance - self.min_distance) * 0.7
                    if self.value < 0.3:  # 亮度最小保持0.3
                        self.value = 0.3
                        
                    print(f"距離: {distance:.1f}cm, 彩度: {self.saturation:.2f}, 亮度: {self.value:.2f}")
                    
                time.sleep(0.2)  # 減少距離讀取頻率，避免訊號干擾
                
            except Exception as e:
                print(f"距離測量發生錯誤: {e}")
                time.sleep(1)  # 錯誤時暫停較久
    
    def display_thread_function(self):
        """主顯示執行緒，負責更新LED顏色"""
        while self.running:
            with self.lock:
                # 根據當前HSV值更新LED顏色
                self.led.set_color_hsv(self.hue, self.saturation, self.value)
            time.sleep(0.1)  # 更新頻率
    
    def start(self):
        """啟動控制系統並開始所有執行緒"""
        print("HSV RGB LED 控制程式啟動")
        print(f"按鈕連接到物理位置 {self.button.pin}")
        print(f"LED 連接到物理位置 紅:{self.led.red_pin}, 綠:{self.led.green_pin}, 藍:{self.led.blue_pin}")
        print(f"超音波感應器連接到 Trig:{self.sensor.trig_pin}, Echo:{self.sensor.echo_pin}")
        print("按下按鈕切換色相，距離控制彩度與亮度")
        print("按下 Ctrl+C 可停止程式")
        
        # 創建並啟動執行緒
        button_thread = threading.Thread(target=self.button_thread_function)
        distance_thread = threading.Thread(target=self.distance_thread_function)
        display_thread = threading.Thread(target=self.display_thread_function)
        
        button_thread.daemon = True
        distance_thread.daemon = True
        display_thread.daemon = True
        
        button_thread.start()
        distance_thread.start()
        display_thread.start()
        
        self.threads = [button_thread, distance_thread, display_thread]
        
        # 設定初始顏色
        self.led.set_color_hsv(self.hue, self.saturation, self.value)
    
    def stop(self):
        """停止控制系統並清理資源"""
        self.running = False    # 通知所有執行緒停止
        time.sleep(0.5)         # 給執行緒時間終止
        
        # 清理資源
        self.led.cleanup()
        GPIO.cleanup()
        print("GPIO 已清理")
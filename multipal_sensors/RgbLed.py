class RgbLed:
    """RGB LED 控制類別"""
    
    def __init__(self, red_pin, green_pin, blue_pin, frequency=1000):
        """初始化 RGB LED
        
        參數:
            red_pin (int): 紅色腳位
            green_pin (int): 綠色腳位
            blue_pin (int): 藍色腳位
            frequency (int): PWM 頻率
        """
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin
        
        # 設定腳位
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)
        
        # 初始化 PWM
        self.red_pwm = GPIO.PWM(self.red_pin, frequency)
        self.green_pwm = GPIO.PWM(self.green_pin, frequency)
        self.blue_pwm = GPIO.PWM(self.blue_pin, frequency)
        
        # 啟動 PWM，初始值為 0（LED 關閉）
        self.red_pwm.start(0)
        self.green_pwm.start(0)
        self.blue_pwm.start(0)
    
    def set_color_rgb(self, r, g, b):
        """設定 RGB LED 的顏色
        
        參數:
            r, g, b (float): 0.0-1.0 的 RGB 值
        """
        # 將 0-1 範圍轉換為 0-100
        r_pwm = int(r * 100)
        g_pwm = int(g * 100)
        b_pwm = int(b * 100)
        
        # 反轉邏輯：0=全亮，100=全暗
        self.red_pwm.ChangeDutyCycle(100 - r_pwm)
        self.green_pwm.ChangeDutyCycle(100 - g_pwm)
        self.blue_pwm.ChangeDutyCycle(100 - b_pwm)
        print(f"RGB設置 - R:{r_pwm}%, G:{g_pwm}%, B:{b_pwm}%")
    
    def set_color_hsv(self, h, s, v):
        """使用HSV值設定LED顏色
        
        參數:
            h (float): 色相 (0.0-1.0)
            s (float): 彩度 (0.0-1.0)
            v (float): 亮度 (0.0-1.0)
        """
        # 轉換HSV到RGB (0-1範圍)
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        self.set_color_rgb(r, g, b)
        print(f"HSV設置 - H:{h:.2f}, S:{s:.2f}, V:{v:.2f}")
    
    def cleanup(self):
        """清理並停止 PWM"""
        self.red_pwm.stop()
        self.green_pwm.stop()
        self.blue_pwm.stop()
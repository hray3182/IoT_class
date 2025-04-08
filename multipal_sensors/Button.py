class Button:
    """按鈕控制類別"""
    
    def __init__(self, pin):
        """初始化按鈕
        
        參數:
            pin (int): 按鈕腳位
        """
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.last_state = GPIO.input(self.pin)
    
    def is_pressed(self):
        """檢測按鈕是否被按下（從 HIGH 到 LOW）
        
        返回:
            bool: 如果按鈕被按下則返回 True，否則返回 False
        """
        current_state = GPIO.input(self.pin)
        pressed = (self.last_state == 1 and current_state == 0)
        self.last_state = current_state
        return pressed
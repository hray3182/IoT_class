import RPi.GPIO as GPIO  # 新增匯入 GPIO 模組
import time  # 新增匯入 time 模組

class UltrasonicSensor:
    """超音波距離感測器類別"""
    
    def __init__(self, trig_pin, echo_pin):
        """初始化超音波感測器
        
        參數:
            trig_pin (int): 觸發腳位
            echo_pin (int): 回應腳位
        """
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        
        # 設定腳位
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
    def set_trigger_pulse(self):
        """產生超音波感應器的觸發脈衝"""
        GPIO.output(self.trig_pin, GPIO.LOW)
        time.sleep(0.000005)
        GPIO.output(self.trig_pin, GPIO.HIGH)
        time.sleep(0.00001)  # 10us
        GPIO.output(self.trig_pin, GPIO.LOW)
    
    def wait_for_echo(self, value, timeout):
        """等待回波訊號變化"""
        count = timeout
        while GPIO.input(self.echo_pin) == value and count > 0:
            count = count - 1
    
    def get_distance(self):
        """測量並返回距離（厘米）"""
        self.set_trigger_pulse()
        self.wait_for_echo(GPIO.LOW, 5000)
        start = time.time()
        self.wait_for_echo(GPIO.HIGH, 5000)
        finish = time.time()
        pulse_len = finish - start
        
        # v = 331 + 0.6 * T (攝氏25度)
        v = 331 + 0.6 * 25
        distance_cm = pulse_len * v * 100 / 2
        return distance_cm
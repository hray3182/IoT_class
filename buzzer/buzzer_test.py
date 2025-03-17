import RPi.GPIO as GPIO
import time

# 設置GPIO模式
GPIO.setmode(GPIO.BOARD)  # 使用物理引腳編號

# 定義蜂鳴器引腳（物理引腳15）
buzzer_pin = 15

# 設置蜂鳴器引腳為輸出
GPIO.setup(buzzer_pin, GPIO.OUT)

try:
    print("蜂鳴器測試開始...")
    
    # 方法1：直接控制高低電平
    print("測試方法1：直接控制高低電平")
    for _ in range(5):
        GPIO.output(buzzer_pin, GPIO.HIGH)  # 打開蜂鳴器
        time.sleep(0.5)
        GPIO.output(buzzer_pin, GPIO.LOW)   # 關閉蜂鳴器
        time.sleep(0.5)
    
    # 方法2：使用PWM模擬不同頻率
    print("測試方法2：使用PWM模擬不同頻率")
    buzzer = GPIO.PWM(buzzer_pin, 1000)
    buzzer.start(50)  # 佔空比為50%
    
    # 播放不同頻率的聲音
    frequencies = [261, 293, 329, 349, 391, 440, 493, 523]  # 音階頻率
    
    for freq in frequencies:
        print(f"播放頻率: {freq}Hz")
        buzzer.ChangeFrequency(freq)
        time.sleep(0.5)
    
    # 停止蜂鳴器
    buzzer.stop()
    
    # 方法3：手動產生方波
    print("測試方法3：手動產生方波")
    for _ in range(10):
        for _ in range(100):  # 產生一個約1kHz的方波
            GPIO.output(buzzer_pin, GPIO.HIGH)
            time.sleep(0.0005)
            GPIO.output(buzzer_pin, GPIO.LOW)
            time.sleep(0.0005)
        time.sleep(0.1)
    
    print("蜂鳴器測試結束")

except KeyboardInterrupt:
    # 當按下Ctrl+C時，停止蜂鳴器並清理GPIO
    print("程序被用戶中斷")

finally:
    # 清理GPIO設置
    GPIO.cleanup()
    print("GPIO已清理") 
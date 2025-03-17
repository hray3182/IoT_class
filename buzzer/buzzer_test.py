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
    
    # 方法1：直流模式（持續高電平）
    print("測試方法1：直流模式（持續高電平）")
    print("持續高電平 5 秒...")
    GPIO.output(buzzer_pin, GPIO.HIGH)  # 打開蜂鳴器，持續高電平
    time.sleep(5)
    GPIO.output(buzzer_pin, GPIO.LOW)   # 關閉蜂鳴器
    time.sleep(1)
    
    # 方法2：直流模式（持續低電平）
    print("測試方法2：直流模式（持續低電平）")
    print("持續低電平 5 秒...")
    GPIO.output(buzzer_pin, GPIO.LOW)  # 持續低電平
    time.sleep(5)
    
    # 方法3：低頻交流模式
    print("測試方法3：低頻交流模式（1Hz）")
    for _ in range(5):
        GPIO.output(buzzer_pin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(buzzer_pin, GPIO.LOW)
        time.sleep(0.5)
    
    # 方法4：中頻交流模式
    print("測試方法4：中頻交流模式（10Hz）")
    for _ in range(50):
        GPIO.output(buzzer_pin, GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(buzzer_pin, GPIO.LOW)
        time.sleep(0.05)
    
    # 方法5：高頻交流模式
    print("測試方法5：高頻交流模式（100Hz）")
    for _ in range(100):
        GPIO.output(buzzer_pin, GPIO.HIGH)
        time.sleep(0.005)
        GPIO.output(buzzer_pin, GPIO.LOW)
        time.sleep(0.005)
    
    # 方法6：PWM模式（可調頻率）
    print("測試方法6：PWM模式（可調頻率）")
    buzzer = GPIO.PWM(buzzer_pin, 1)  # 從1Hz開始
    buzzer.start(50)  # 佔空比為50%
    
    # 測試不同的PWM頻率
    pwm_freqs = [1, 5, 10, 50, 100, 500, 1000]
    for freq in pwm_freqs:
        print(f"PWM頻率: {freq}Hz")
        buzzer.ChangeFrequency(freq)
        time.sleep(3)
    
    # 停止蜂鳴器
    buzzer.stop()
    
    print("蜂鳴器測試結束")

except KeyboardInterrupt:
    # 當按下Ctrl+C時，停止蜂鳴器並清理GPIO
    try:
        buzzer.stop()
    except:
        pass
    print("程序被用戶中斷")

finally:
    # 清理GPIO設置
    GPIO.cleanup()
    print("GPIO已清理") 
import RPi.GPIO as GPIO
import time

# 設置GPIO模式
GPIO.setmode(GPIO.BOARD)  # 使用物理引腳編號

# 定義蜂鳴器引腳（物理引腳15）
buzzer_pin = 15

# 設置蜂鳴器引腳為輸出
GPIO.setup(buzzer_pin, GPIO.OUT)

# 創建PWM對象，頻率為1000Hz
buzzer = GPIO.PWM(buzzer_pin, 1000)

try:
    print("蜂鳴器測試開始...")
    
    # 啟動蜂鳴器
    buzzer.start(50)  # 佔空比為50%
    
    # 播放不同頻率的聲音
    frequencies = [261, 293, 329, 349, 391, 440, 493, 523]  # 音階頻率
    
    for freq in frequencies:
        print(f"播放頻率: {freq}Hz")
        buzzer.ChangeFrequency(freq)
        time.sleep(0.5)
    
    # 播放警報聲
    print("播放警報聲...")
    for _ in range(5):
        buzzer.ChangeFrequency(800)
        time.sleep(0.2)
        buzzer.ChangeFrequency(600)
        time.sleep(0.2)
    
    # 停止蜂鳴器
    buzzer.stop()
    print("蜂鳴器測試結束")

except KeyboardInterrupt:
    # 當按下Ctrl+C時，停止蜂鳴器並清理GPIO
    buzzer.stop()
    print("程序被用戶中斷")

finally:
    # 清理GPIO設置
    GPIO.cleanup()
    print("GPIO已清理") 
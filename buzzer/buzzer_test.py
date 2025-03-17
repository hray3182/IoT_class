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
    
    # 方法2：使用PWM模擬不同頻率（改進版）
    print("測試方法2：使用PWM模擬不同頻率（改進版）")
    buzzer = GPIO.PWM(buzzer_pin, 261)  # 從第一個頻率開始
    buzzer.start(50)  # 佔空比為50%
    
    # 播放不同頻率的聲音
    frequencies = [261, 293, 329, 349, 391, 440, 493, 523]  # 音階頻率
    
    # 使用更長的持續時間和漸變效果
    for freq in frequencies:
        print(f"播放頻率: {freq}Hz")
        buzzer.ChangeFrequency(freq)
        time.sleep(1)  # 延長每個音符的持續時間
    
    # 播放一個簡單的旋律
    print("播放簡單旋律...")
    melody = [261, 261, 391, 391, 440, 440, 391, 0,  # 小星星
              349, 349, 329, 329, 293, 293, 261, 0]
    durations = [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.6, 0.1,
                0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.6, 0.1]
    
    for i in range(len(melody)):
        if melody[i] == 0:  # 休止符
            buzzer.stop()
            time.sleep(durations[i])
            if i < len(melody) - 1 and melody[i+1] != 0:  # 如果下一個音不是休止符
                buzzer.start(50)
        else:
            buzzer.ChangeFrequency(melody[i])
            time.sleep(durations[i])
    
    # 停止蜂鳴器
    buzzer.stop()
    
    # 方法3：手動產生方波（改進版）
    print("測試方法3：手動產生方波（改進版）")
    
    # 使用更精確的時間控制
    def play_tone(frequency, duration):
        period = 1.0 / frequency
        delay = period / 2
        cycles = int(frequency * duration)
        
        for i in range(cycles):
            GPIO.output(buzzer_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(buzzer_pin, GPIO.LOW)
            time.sleep(delay)
    
    # 播放一個音階
    scale = [261, 293, 329, 349, 391, 440, 493, 523]
    for freq in scale:
        print(f"手動產生頻率: {freq}Hz")
        play_tone(freq, 0.5)
        time.sleep(0.1)
    
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
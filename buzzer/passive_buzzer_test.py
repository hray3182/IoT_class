import RPi.GPIO as GPIO
import time

# 設置GPIO模式
GPIO.setmode(GPIO.BOARD)  # 使用物理引腳編號

# 定義蜂鳴器引腳（物理引腳15）
buzzer_pin = 15

# 設置蜂鳴器引腳為輸出
GPIO.setup(buzzer_pin, GPIO.OUT)

# 無源蜂鳴器需要使用PWM來產生聲音
# 創建PWM對象，初始頻率為1000Hz
buzzer = GPIO.PWM(buzzer_pin, 1000)

try:
    print("無源蜂鳴器測試開始...")
    print("注意：無源蜂鳴器需要交流信號才能發聲")
    print("如果聲音太小，可以嘗試將蜂鳴器連接到5V而不是3.3V")
    
    # 啟動PWM，佔空比為50%
    buzzer.start(50)
    
    # 測試1：掃描頻率範圍（找出最佳共振頻率）
    print("\n測試1：掃描頻率範圍（找出最佳共振頻率）")
    print("從低頻到高頻掃描，請注意哪個頻率聲音最大...")
    
    # 無源蜂鳴器通常在2000-5000Hz範圍內效果最好
    freq_ranges = [
        (100, 1000, 100),    # 100Hz到1000Hz，步進100Hz
        (1000, 3000, 200),   # 1000Hz到3000Hz，步進200Hz
        (3000, 5000, 200),   # 3000Hz到5000Hz，步進200Hz
        (5000, 10000, 500)   # 5000Hz到10000Hz，步進500Hz
    ]
    
    for start, end, step in freq_ranges:
        for freq in range(start, end, step):
            print(f"測試頻率: {freq}Hz")
            buzzer.ChangeFrequency(freq)
            time.sleep(0.5)
    
    # 測試2：常見音樂音符頻率
    print("\n測試2：常見音樂音符頻率")
    notes = {
        "C4 (中央C)": 262,
        "D4": 294,
        "E4": 330,
        "F4": 349,
        "G4": 392,
        "A4": 440,
        "B4": 494,
        "C5": 523
    }
    
    for note, freq in notes.items():
        print(f"播放音符: {note} ({freq}Hz)")
        buzzer.ChangeFrequency(freq)
        time.sleep(1)
    
    # 測試3：播放簡單旋律（小星星）
    print("\n測試3：播放簡單旋律（小星星）")
    melody = [262, 262, 392, 392, 440, 440, 392, 0, 
              349, 349, 330, 330, 294, 294, 262, 0]
    durations = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.2,
                0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.2]
    
    for i in range(len(melody)):
        if melody[i] == 0:  # 休止符
            buzzer.stop()
            time.sleep(durations[i])
            if i < len(melody) - 1 and melody[i+1] != 0:
                buzzer.start(50)
        else:
            buzzer.ChangeFrequency(melody[i])
            time.sleep(durations[i])
    
    # 測試4：測試不同佔空比（音量控制）
    print("\n測試4：測試不同佔空比（音量控制）")
    # 使用最佳頻率（假設為2500Hz，您可以根據之前的測試調整）
    best_freq = 2500
    buzzer.ChangeFrequency(best_freq)
    
    for duty in [10, 30, 50, 70, 90]:
        print(f"佔空比: {duty}%")
        buzzer.ChangeDutyCycle(duty)
        time.sleep(1)
    
    # 測試5：警報聲
    print("\n測試5：警報聲")
    for _ in range(5):
        buzzer.ChangeFrequency(2500)
        time.sleep(0.2)
        buzzer.ChangeFrequency(2000)
        time.sleep(0.2)
    
    # 停止蜂鳴器
    buzzer.stop()
    
    print("\n無源蜂鳴器測試結束")
    print("建議：")
    print("1. 如果聲音太小，請嘗試將蜂鳴器連接到5V而不是3.3V")
    print("2. 記下聲音最大的頻率，用於未來的項目")
    print("3. 無源蜂鳴器需要PWM信號才能正常工作")

except KeyboardInterrupt:
    # 當按下Ctrl+C時，停止蜂鳴器並清理GPIO
    buzzer.stop()
    print("\n程序被用戶中斷")

finally:
    # 清理GPIO設置
    GPIO.cleanup()
    print("GPIO已清理") 
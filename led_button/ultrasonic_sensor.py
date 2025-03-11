import RPi.GPIO as GPIO
import time

# 設定 GPIO 腳位
TRIG = 40      # 觸發腳位 (Trig)
ECHO = 38      # 回應腳位 (Echo)
BUZZER_PIN = 36  # 蜂鳴器腳位

GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

def measure_distance():
    """ 測量超音波傳回的距離 (公分) """
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 產生 10µs 的觸發脈衝
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    pulse_end = time.time()  # 確保變數已定義

    timeout = time.time() + 0.02  # 設定 20ms 超時
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return -1  # 超時返回 -1

    timeout = time.time() + 0.02  # 重新設定 20ms 超時
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return -1  # 超時返回 -1

    # 計算脈衝持續時間
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # 17150 = 34300 cm/s ÷ 2
    distance = round(distance, 2)  # 取兩位小數

    if distance > 400:  
        return -1  # 忽略異常數據

    return distance

try:
    while True:
        distance = measure_distance()
        
        if distance != -1:  # 只顯示正常數據
            print(f"測得距離: {distance} cm")
            
            if distance < 30:
                GPIO.output(BUZZER_PIN, True)  # 蜂鳴器響
                print("物體太近！蜂鳴器響起！")
            else:
                GPIO.output(BUZZER_PIN, False)  # 蜂鳴器停止
            
        time.sleep(0.5)  

except KeyboardInterrupt:
    print("程式已停止")

finally:
    GPIO.cleanup()

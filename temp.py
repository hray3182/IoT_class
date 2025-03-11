import sys
import smbus
import time

# LM75A 的默認 I2C 地址
address = 0x48
LM75_TEMP_REGISTER = 0

# 初始化 I2C 總線
bus = smbus.SMBus(1)

try:
    while True:
        # 直接讀取字數據並保留 16 位
        raw = bus.read_word_data(address, LM75_TEMP_REGISTER) & 0xFFFF
        
        # SWAP LSB 和 MSB
        raw = ((raw << 8) & 0xFF00) + (raw >> 8)
        
        # 只有 9 位包含溫度數據，右移 7 位
        raw = raw >> 7
        
        # 溫度刻度為 0.5
        temperature = raw / 2
        
        print(f"溫度: {temperature:.2f}°C")
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\n程序已停止")

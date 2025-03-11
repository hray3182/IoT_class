import smbus
import time

class LM75A:
    # LM75A 的默認 I2C 地址
    DEVICE_ADDRESS = 0x48
    
    # 溫度寄存器地址
    TEMP_REGISTER = 0x00
    
    def __init__(self, bus_number=1):
        """初始化 LM75A"""
        self.bus = smbus.SMBus(bus_number)
    
    def read_temperature(self):
        """讀取溫度值
        
        返回:
            float: 攝氏溫度值
        """
        # 讀取兩個字節的溫度數據
        raw_data = self.bus.read_i2c_block_data(self.DEVICE_ADDRESS, self.TEMP_REGISTER, 2)
        
        # 將兩個字節組合成 16 位整數
        raw = (raw_data[0] << 8) | raw_data[1]
        
        # SWAP LSB 和 MSB
        raw = ((raw << 8) & 0xFF00) + (raw >> 8)
        
        # 只有 9 位包含溫度數據，右移 7 位
        raw = raw >> 7
        
        # 溫度刻度為 0.5
        temperature = raw / 2
        
        return temperature

if __name__ == "__main__":
    # 創建 LM75A 實例
    sensor = LM75A()
    
    try:
        while True:
            # 讀取溫度
            temp = sensor.read_temperature()
            print(f"當前溫度: {temp:.2f}°C")
            
            # 每秒更新一次
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n程序已停止")

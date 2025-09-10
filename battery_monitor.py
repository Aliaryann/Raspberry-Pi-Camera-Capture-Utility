import smbus2
import time

# Set up I2C communication with the battery
I2C_ADDR = 0x36
bus = smbus2.SMBus(1)

def read_battery():
    # Read voltage and capacity (based on X728 docs)
    #voltage_raw = bus.read_word_data(I2C_ADDR, 0x02)
    capacity_raw = bus.read_word_data(I2C_ADDR, 0x04)
    
    # Swap bytes (UPS often returns reversed data)
    #voltage = ((voltage_raw & 0xFF) << 8) + (voltage_raw >> 8)
    capacity = ((capacity_raw & 0xFF) << 8) + (capacity_raw >> 8)
    
    # Convert to meaningful units (mV and percentage)
    #voltage = voltage * 1.12 / 10000
    capacity = capacity / 256
    return capacity

if __name__ == "__main__":
    while True:
        voltage, capacity = read_battery()
        print(f"Capacity: {capacity}%")
        time.sleep(1)



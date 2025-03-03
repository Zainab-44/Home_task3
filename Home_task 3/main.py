from machine import Pin, SoftI2C
import ssd1306
import dht
import time

# I2C Configuration
I2C_SCL = 9  # Change if needed
I2C_SDA = 8  # Change if needed

# Initialize SoftI2C
i2c = SoftI2C(scl=Pin(I2C_SCL), sda=Pin(I2C_SDA))

# Scan for I2C devices
devices = i2c.scan()
oled = None


if devices:
    print(f"✅ I2C device(s) found: {[hex(device) for device in devices]}")
    try:
        oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)  # Change to 0x3D if needed
    except OSError as e:
        print("❌ OLED Initialization Failed:", e)
else:
    print("⚠️ No I2C device found! Check wiring!")

# Initialize DHT22 Sensor
DHT_PIN = 4
dht_sensor = dht.DHT22(Pin(DHT_PIN))

def display_oled(temp, humidity):
    """Display temperature and humidity on the OLED screen."""
    if oled:
        oled.fill(0)  # Clear screen
        oled.text(f"Temp: {temp:.1f}C", 0, 0)
        oled.text(f"Humidity: {humidity:.1f}%", 0, 16)
        oled.text("Status: OK", 0, 32)
        oled.show()
    else:
        print("⚠️ OLED not initialized. Skipping display update.")

while True:
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        humidity = dht_sensor.humidity()

        print(f"🌡️ Temp: {temp:.1f}°C | 💧 Humidity: {humidity:.1f}%")
        display_oled(temp, humidity)

    except OSError as e:
        print("⚠️ Error reading DHT22 sensor:", e)
        if oled:
            oled.fill(0)
            oled.text("Sensor Error!", 0, 0)
            oled.show()
    
    time.sleep(2)  # Wait for 2 seconds

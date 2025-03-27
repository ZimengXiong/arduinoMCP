import serial
import threading
import time
# Initialize the MCP server

# Initialize serial communication with the Arduino
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Create a lock to handle race conditions for serial communication
serial_lock = threading.Lock()

with serial_lock:
    ser.write(b"0\n")
    color = ser.readline().decode().strip()

print(f"Current RGB color is {color}")

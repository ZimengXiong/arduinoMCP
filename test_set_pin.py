import serial
import threading
import time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

serial_lock = threading.Lock()

def test_set_pin(pin: int, state: str):
    """
    Test function to set a GPIO pin HIGH or LOW.
    state: 'H' or 'L' (case insensitive)
    """
    state = state.upper()
    if state not in ('H', 'L'):
        print("Invalid state. Use 'H' for HIGH or 'L' for LOW.")
        return
    
    command = f"P{pin}{state}\n"
    
    with serial_lock:
        ser.write(command.encode())
        time.sleep(0.1)  
        response = ser.readline().decode().strip()
    
    print(f"Sent command: {command.strip()} | Arduino response: {response}")

if __name__ == "__main__":
    time.sleep(2) 
    test_set_pin(13, 'H')
    time.sleep(1)
    test_set_pin(13, 'L') 

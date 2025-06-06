import serial
import threading
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("RGBLightController")

# Initialize serial communication with the Arduino
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Create a lock to handle race conditions for serial communication
serial_lock = threading.Lock()

# Define a tool to set the RGB light color
@mcp.tool()
def set_rgb_color(red: int, green: int, blue: int) -> str:
    """Set the RGB light to the specified color."""
    # Validate that RGB values are within the acceptable range
    if not all(0 <= val <= 255 for val in (red, green, blue)):
        return "Error: RGB values must be between 0 and 255."
    
    # Format each color component to be a 3-digit number with leading zeros if necessary
    command = f"{red:03}{green:03}{blue:03}\n"
    
    # Use the lock to ensure only one thread accesses the serial port at a time
    with serial_lock:
        ser.write(command.encode())
    
    return f"Set RGB color to Red: {red}, Green: {green}, Blue: {blue}"

# Define a tool to retrieve the current RGB color
@mcp.tool()
def get_current_color() -> str:
    """Get the current RGB color from the light."""
    serial_lock = threading.Lock()

    with serial_lock:
        ser.write(b"0\n")
        color = ser.readline().decode().strip()

    return f"Current RGB color is {color}"

def set_gpio_pin(pin: int, state: str) -> str:
    """Set a GPIO pin to HIGH or LOW."""
    state = state.upper()
    if state not in ["H", "L"]:
        return "Error: State must be 'H' or 'L'."
    if not (0 <= pin <= 53):  # Valid for Uno/Mega
        return "Error: Invalid GPIO pin number."

    command = f"P{pin}{state}\n"

    with serial_lock:
        ser.write(command.encode())

    return f"Set pin {pin} to {'HIGH' if state == 'H' else 'LOW'}"
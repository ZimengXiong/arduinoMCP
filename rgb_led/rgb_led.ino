#include <Adafruit_NeoPixel.h>

int Power = 11;
int PIN  = 12;
#define NUMPIXELS 1

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  pixels.begin();
  pinMode(Power, OUTPUT);
  digitalWrite(Power, HIGH);
  Serial.begin(9600); // Initialize serial communication at 9600 baud rate
}

void loop() { 
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n'); // Read until newline
    input.trim(); // Remove any whitespace or newline chars

    if (input.length() == 9 && input.toInt() != 0) { // RGB set: 9 digits
      int red = input.substring(0, 3).toInt();
      int green = input.substring(3, 6).toInt();
      int blue = input.substring(6, 9).toInt();
      setColor(red, green, blue);
    } else if (input.length() == 1 && input == "C") {
      getColor();
    } else if (input.startsWith("P")) { // SetPin command
      parseSetPinCommand(input);
    } else {
      Serial.println("Invalid command");
    }
  }
}

void setColor(int red, int green, int blue) {
  pixels.setPixelColor(0, pixels.Color(red, green, blue));
  pixels.show();
}

void getColor() {
  uint32_t color = pixels.getPixelColor(0);
  int red = (color >> 16) & 0xFF;
  int green = (color >> 8) & 0xFF;
  int blue = color & 0xFF;
  Serial.print("Current Color - Red: ");
  Serial.print(red);
  Serial.print(", Green: ");
  Serial.print(green);
  Serial.print(", Blue: ");
  Serial.println(blue);
}

void setPin(int gpio, bool state) {
  pinMode(gpio, OUTPUT);
  digitalWrite(gpio, state ? HIGH : LOW);
}

void parseSetPinCommand(String cmd) {
  if (cmd.length() < 3) {
    Serial.println("Invalid SetPin format");
    return;
  }

  int pin = cmd.substring(1, cmd.length() - 1).toInt();
  char stateChar = cmd.charAt(cmd.length() - 1);
  bool state;

  if (stateChar == 'H' || stateChar == 'h') {
    state = true;
  } else if (stateChar == 'L' || stateChar == 'l') {
    state = false;
  } else {
    Serial.println("Invalid pin state");
    return;
  }

  setPin(pin, state);
  Serial.print("Set pin ");
  Serial.print(pin);
  Serial.print(" to ");
  Serial.println(state ? "HIGH" : "LOW");
}

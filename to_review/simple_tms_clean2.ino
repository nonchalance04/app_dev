/*
  Traffic Light Controller - Arduino Code
  Simple version that works with Python GUI
  
  Commands from Python:
  - 'R' = Red light ON
  - 'Y' = Yellow light ON  
  - 'G' = Green light ON
  - 'S' = Stop/Turn off all lights
*/

// LED pin definitions
int redLED = 8;
int yellowLED = 9;
int greenLED = 10;

void setup() {
  // Start serial communication at 9600 baud
  Serial.begin(9600);
  
  // Set LED pins as outputs
  pinMode(redLED, OUTPUT);
  pinMode(yellowLED, OUTPUT);
  pinMode(greenLED, OUTPUT);
  
  // Turn off all LEDs at start
  turnOffAllLights();
  
  // Send ready message to Python
  Serial.println("Arduino Traffic Light Ready!");
  delay(100);
}

void loop() {
  // Check for commands from Python
  if (Serial.available() > 0) {
    char command = Serial.read();
    processCommand(command);
  }
  
  // Small delay to prevent overwhelming serial communication
  delay(10);
}

void processCommand(char cmd) {
  switch (cmd) {
    case 'R':
      // Red command from Python
      turnOnRed();
      Serial.println("Red ON");
      break;
      
    case 'Y': 
      // Yellow command from Python
      turnOnYellow();
      Serial.println("Yellow ON");
      break;
      
    case 'G':
      // Green command from Python
      turnOnGreen();
      Serial.println("Green ON");
      break;
      
    case 'S':
      // Stop command from Python
      turnOffAllLights();
      Serial.println("All lights OFF");
      break;
      
    default:
      // Unknown command - ignore silently
      break;
  }
}

void turnOnRed() {
  digitalWrite(redLED, HIGH);
  digitalWrite(yellowLED, LOW);
  digitalWrite(greenLED, LOW);
}

void turnOnYellow() {
  digitalWrite(redLED, LOW);
  digitalWrite(yellowLED, HIGH);
  digitalWrite(greenLED, LOW);
}

void turnOnGreen() {
  digitalWrite(redLED, LOW);
  digitalWrite(yellowLED, LOW);
  digitalWrite(greenLED, HIGH);
}

void turnOffAllLights() {
  digitalWrite(redLED, LOW);
  digitalWrite(yellowLED, LOW);
  digitalWrite(greenLED, LOW);
}
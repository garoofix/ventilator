// Author:  David Garufi, April 2020
// Ventilator proof of concept control

#include <SPI.h>

// Define stepper motor connections:
#define dirPin           7                // Motor direction pin
#define stepPin          5                // Motor step pin
#define enPin            6                // Motor enable
#define homePin         13                // Home flag
// Other definitions
#define pitch            5.0              // mm per rotation of lead screw
#define stepperN       200.0              // Steps in stepper motor rotation

#define INPUT_SIZE      30
int sdata              = 0;               // for incoming serial data
void setup() {
  Serial.begin(9600);

  // Declare pins
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(enPin, OUTPUT);
  pinMode(homePin, INPUT);
  
  digitalWrite(dirPin, HIGH);  // LOW = COMPRESS, HIGH = REPRESSURIZE
  digitalWrite(enPin, HIGH);
  toggleDirection();
}

int dir = 0;
int en = 1;
int encoder = 0;
void loop(void) {
  // 
  findCmd();

  // do stuff with command:
  // - perform a homing sequence
  // - move axis by delta-mm @ speed
  // - move axis to absolute position (mm) @ speed
  // - maybe a couple other similar commands
}

void findCmd(){
  // Some function to parse a serial cmd in the format:
  // <CMD><AXIS> <VALUE>;
  // Ex "X1 5.0;" to move axis 1 (1) by a delta (X) of 5mm
}

void moveDelta(float dist){
  float dPerStep          = pitch / stepperN;
  int nSteps              = dist / dPerStep;
  if(nSteps < 0){
    nSteps = nSteps * -1;
    digitalWrite(dirPin, HIGH);
  }else{
    digitalWrite(dirPin, LOW);
  }

  for (int i = 0; i < nSteps; i++){
    step();
    // Still working on homing sequence and limit switch logic
    if(digitalRead(homePin) == 1){
      encoder = 0;
      delay(1000);
      break;
    }
  }
  Serial.println(nSteps);
}

void homeSequence(){
  // This doesn't work like it's supposed to yet.  Still playing
  digitalWrite(dirPin, LOW);     // Set direction to compress
  delay(100);
  for (int j = 0; j < 16; j++){
    for (int i = 0; i < 200; i++){
      step();
      if(digitalRead(homePin) == 1){
        encoder = 0;
        delay(1000);
        break;
      }
    }
  }

  digitalWrite(dirPin, LOW);     // Set direction to repressurize
  delay(100);
  // Rotate 1 back
  for (int i = 0; i < 200; i++){step();}
}

void toggleDirection(){
  if(dir == 1) {
    digitalWrite(dirPin, LOW); dir = 0;
    Serial.println("DIRECTION: POS");
  }else{
    digitalWrite(dirPin, HIGH); dir = 1;
    Serial.println("DIRECTION: NEG");
  }
}

void toggleEnable(){
  if(en == 1) {
    digitalWrite(enPin, LOW); en = 0;
    Serial.println("** MOTOR DISABLED **");
  }else{
    digitalWrite(enPin, HIGH); en = 1;
    Serial.println("** MOTOR ENABLED **");
  }
}

// Steps the stepper motor.
// Will need to dynamically change the step speed, but for now is static
void step() {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(550);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(550);
}

//DHTlib by rob
#include <dht.h>
#define DHT11_PIN 8
#include <Stepper.h>
dht DHT;

#include <Wire.h>

#include <sdpsensor.h>

SDP8XXSensor sdp;

String str;

int steps;
const int xdrev=1; // distance [cm] traveled per revolution
const int ydrev=1; // distance [cm] traveled per revolution 
const int stepsPerRevolution = 2038;
const int xlength=10;
const int ylength=10;
Stepper xstepper = Stepper(stepsPerRevolution, 9, 11, 10, 12);
Stepper ystepper = Stepper(stepsPerRevolution, 4,6,5,7);
const byte xswitch = 2;
const byte yswitch = 3;


int i;
int delay1;

void setup() {
  // put your setup code here, to run once:
  Wire.begin();
  Serial.begin(115200);
  Serial.setTimeout(10);
  Serial.flush();
  attachInterrupt(0, xstop, HIGH); //Pin 2 switch with pull up resistor
  attachInterrupt(1, ystop, HIGH); //Pin 3 switch with pull up resistor
}


void loop() {
  
 int chk = DHT.read11(DHT11_PIN);
 if (Serial.available() >0){
  str = Serial.readStringUntil('\n');
  //Serial.flush();
  if (str=="temp"){
    delay(1000);
    i=Serial.parseInt();
    for (int x=0; x<i; x++){
      Serial.print(DHT.temperature);
      Serial.print("\n");
      delay(1000);
    }
  }

    if (str=="hmd"){
    delay(1000);
    i=Serial.parseInt();
    for (int x=0; x<i; x++){
      Serial.print(DHT.humidity);
      Serial.print("\n");
      delay(1000);
    }
 }
    
 if(str=="homex"){
    delay(100);
    Serial.print("homex");
    xstepper.setSpeed(10);
    xstepper.step(-500);
    steps=stepsPerRevolution*xdrev*xlength;
    xstepper.step(steps);
      }
 if(str=="homey"){
    delay(100);
    ystepper.setSpeed(10);
    ystepper.step(-500);
    steps=stepsPerRevolution*ydrev*ylength;
    ystepper.step(steps);
      }
 if(str=="xpositive"){
    delay(1000);
    xstepper.setSpeed(10);
    i=Serial.parseInt();
    steps=stepsPerRevolution*xdrev*i;
    xstepper.step(steps);
      }
  if(str=="ypositive"){
    delay(1000);
    ystepper.setSpeed(10);
    i=Serial.parseInt();
    steps=stepsPerRevolution*ydrev*i;
    ystepper.step(steps);
      }
   if(str=="xnegative"){
    delay(1000);
    xstepper.setSpeed(10);
    i=Serial.parseInt();
    steps=stepsPerRevolution*xdrev*i;
    xstepper.step(-steps);
      }
   if(str=="ynegative"){
    delay(1000);
    ystepper.setSpeed(10);
    i=Serial.parseInt();
    steps=stepsPerRevolution*ydrev*i;
    ystepper.step(-steps);
      }
   if (str=="pressure"){
    delay(1000);
    i=Serial.parseInt();
    Serial.flush();
    delay(1000);
    delay1=Serial.parseInt();
    for (int x=0; x<i; x++){
      sdp.readSample();
      Serial.print(sdp.getDifferentialPressure());
      Serial.print("\n");
      delay(delay1);
    }
  }
}
}
void xstop() {
  xstepper.setSpeed(0);
}

void ystop() {
  ystepper.setSpeed(0);
}

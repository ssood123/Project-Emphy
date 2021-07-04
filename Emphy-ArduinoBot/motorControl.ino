#include <AFMotor.h>
#include <Servo.h> 
#include <NewPing.h>

#define TRIG_PIN A0
#define ECHO_PIN A1
#define MAX_DISTANCE_POSSIBLE 100 
#define MAX_SPEED 160
#define MOTORS_CALIBRATION_OFFSET 3
#define COLL_DIST 20 ....................................................................................................................
#define TURN_DIST COLL_DIST+10 
#define trigPin A0
#define echoPin A1

AF_DCMotor leftFrontMotor(1, MOTOR12_8KHZ); 
AF_DCMotor rightFrontMotor(2, MOTOR12_8KHZ); 
AF_DCMotor rightBackMotor(3, MOTOR34_8KHZ); 
AF_DCMotor leftBackMotor(4, MOTOR34_8KHZ);
Servo headServo;

int speedSet =165;
//forwardPin=A3;
//rightPin=A4;
//leftPin=A5;

void setup() {
  // put your setup code here, to run once:
  leftFrontMotor.setSpeed(speedSet);
  rightFrontMotor.setSpeed(speedSet);
  rightBackMotor.setSpeed(speedSet);
  leftBackMotor.setSpeed(speedSet);
  pinMode(A3,INPUT_PULLUP);
  pinMode(A4,INPUT_PULLUP);
  pinMode(A5,INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(digitalRead(A3)==1 && digitalRead(A4)==0 && digitalRead(A5)==0){
    Serial.println("forward");
    //forward
    leftFrontMotor.setSpeed(speedSet);
    rightFrontMotor.setSpeed(speedSet);
    rightBackMotor.setSpeed(speedSet);
    leftBackMotor.setSpeed(speedSet);
    leftFrontMotor.run(BACKWARD);
    rightFrontMotor.run(BACKWARD);
    leftBackMotor.run(FORWARD);
    rightBackMotor.run(FORWARD);
    
  }
  while(digitalRead(A3)==0 && digitalRead(A4)==0 && digitalRead(A5)==1){
    Serial.println("right");
    //turning right
    leftFrontMotor.setSpeed(speedSet);
    rightFrontMotor.setSpeed(speedSet);
    rightBackMotor.setSpeed(speedSet);
    leftBackMotor.setSpeed(speedSet);
    leftFrontMotor.run(BACKWARD);
    rightFrontMotor.run(FORWARD);
    leftBackMotor.run(FORWARD);
    rightBackMotor.run(BACKWARD);
    delay(200);
    leftFrontMotor.run(RELEASE);
    rightFrontMotor.run(RELEASE);
    leftBackMotor.run(RELEASE);
    rightBackMotor.run(RELEASE);
    delay(200);
  }
  while(digitalRead(A3)==0 && digitalRead(A4)==1 && digitalRead(A5)==0){
    Serial.println("left");
    //turning left
    leftFrontMotor.setSpeed(speedSet);
    rightFrontMotor.setSpeed(speedSet);
    rightBackMotor.setSpeed(speedSet);
    leftBackMotor.setSpeed(speedSet);
    leftFrontMotor.run(FORWARD);
    rightFrontMotor.run(BACKWARD);
    leftBackMotor.run(BACKWARD);
    rightBackMotor.run(FORWARD);
    delay(200);
    leftFrontMotor.run(RELEASE);
    rightFrontMotor.run(RELEASE);
    leftBackMotor.run(RELEASE);
    rightBackMotor.run(RELEASE);
    delay(200);
  }
  while(not((digitalRead(A3)==1 && digitalRead(A4)==0 && digitalRead(A5)==0)||(digitalRead(A3)==0 && digitalRead(A4)==0 && digitalRead(A5)==1)||(digitalRead(A3)==0 && digitalRead(A4)==1 && digitalRead(A5)==0))){
    Serial.println("no movement");
    //no input
    leftFrontMotor.setSpeed(130);
    rightFrontMotor.setSpeed(130);
    rightBackMotor.setSpeed(130);
    leftBackMotor.setSpeed(130);
    leftFrontMotor.run(FORWARD);
    rightFrontMotor.run(BACKWARD);
    leftBackMotor.run(FORWARD);
    rightBackMotor.run(BACKWARD);
  }
  
}

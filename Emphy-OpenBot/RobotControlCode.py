#include <AFMotor.h>
#include <Servo.h> 
#include <EEPROM.h>

#define MAX_DISTANCE_POSSIBLE 100 
#define MAX_SPEED 160
#define MOTORS_CALIBRATION_OFFSET 3
#define COLL_DIST 20
#define TURN_DIST COLL_DIST+10 
#define trigPin A0
#define echoPin A1

AF_DCMotor leftFrontMotor(1, MOTOR12_8KHZ); 
AF_DCMotor rightFrontMotor(2, MOTOR12_8KHZ); 
AF_DCMotor rightBackMotor(3, MOTOR34_8KHZ); 
AF_DCMotor leftBackMotor(4, MOTOR34_8KHZ);
Servo headServo;


int speedSetRight = 150;
int speedSetLeft = 150;
long duration, distance;
int facing;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(2000000);
  headServo.attach(10);  
  headServo.write(90); 
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  leftFrontMotor.setSpeed(speedSetLeft);
  rightFrontMotor.setSpeed(speedSetRight);
  rightBackMotor.setSpeed(speedSetRight);
  leftBackMotor.setSpeed(speedSetLeft);

  int turnangles[25][10]={ { },
{ 10 },
{ 23 , -90 , 10 },
{ 22 , 45 , 5 , 45 , 17 },
{ 10 },
{ 10 },
{ },
{ 12 , -90 , 10 },
{ 12 , -90 , 28 },
{ 1 , -45 , 7 , 45 , 45 , 7 },
{ 10 , 90 , 23 },
{ 10 , 90 , 12 },
{ },
{ 17 },
{ 10 , 90 , 20 , 45 , 2 , 45 , 7 },
{ 17 , -45 , 5 , -45 , 22 },
{ 28 , 90 , 12 },
{ 17 },
{ },
{ 19 , -45 , 3 , -45 , 13 },
{ 10 },
{ 7 , -45 , 2 , -45 , 7 },
{ 7 , -45 , 2 , -45 , 20 , -90 , 10 },
{ 13 , 45 , 3 , 45 , 19 },
{ },
};
int pathinfo[25]={0 ,1 ,3 ,5 ,1 ,1 ,0 ,3 ,3 ,6 ,3 ,3 ,0 ,1 ,7 ,5 ,3 ,1 ,0 ,5 ,1 ,5 ,7 ,5,0};

int firstFace[25]={ 9 ,2 ,2 ,4 ,4 ,6 ,9 ,2 ,2 ,5 ,0 ,0 ,9 ,4 ,0 ,6 ,0 ,0 ,9 ,6 ,0 ,0 ,0 ,4 ,9 ,};
  // put your main code here, to run repeatedly:
  int locations=5;
  
  int starting= EEPROM.read(1);
  facing = EEPROM.read(0);
  int ending= 3;
  int indexer=starting*locations+ending;
  
  int pathlength=pathinfo[indexer];
  
  int navstep=0;
  int firstturn=calcFirstTurn(facing,firstFace[indexer]);
  performTurn(firstturn);
  Serial.print(firstturn);
  moveForward(1);
  for(int navstep=0;navstep<pathlength;navstep++){
      Serial.print(navstep);
      int turn = turnangles[indexer][navstep];
      if(turn%45!=0){
        moveForward(turn);
      }
      if(turn%45==0){
        performTurn(turn);
        trackFacing(facing,turn);
        moveStop(2000);
        moveForward(1); 
      }      
  } 
  moveStop(100000000); 
}

void loop() {

}

void performTurn(int angle){

  switch (angle) {
    case 0:
      break;
    case 45:
      pos45();
      break;
    case 90:
      pos90();
      break;
    case 135:
      pos135();
      break;
    case 180:
      pos180();
      break;
    case -45:
      neg45();
      break;
    case -90:
      neg90();
      break;
    case -135:
      neg135();
      break;
    }
}

int calcFirstTurn(int facing,int needtoface){
  //String dir[8]={"north","northeast","east","southeast","south","southwest","west","northwest"};
  int turn=0;
  int difference=facing-needtoface;
  if(difference>4){
    turn=-45*(8-difference);
  }
  if(difference<-3){
    turn=45*(8+difference);
  }
  if(-3<=difference<=4){
    turn=45*difference;
  }
  facing=needtoface;
  return turn;  
}

void trackFacing(int curface,int turn){
  //String dir[8]={"north","northeast","east","southeast","south","southwest","west","northwest"};
  int jump=turn/45;
  int changed=0;
  if (facing==0 && turn<0){
    facing=8+jump;
    changed=1;
  }
  if(facing==7 && turn>0){
    facing=jump;
    changed=1;
  }
  if(changed==0){
    facing=facing+jump;
  }
  
}


void neg90(){
  leftFrontMotor.setSpeed(250);
  rightFrontMotor.setSpeed(250);
  leftBackMotor.setSpeed(250);
  leftFrontMotor.run(BACKWARD);
  rightFrontMotor.run(FORWARD);
  rightBackMotor.run(FORWARD);
  leftBackMotor.run(FORWARD);
  delay(600);
  leftFrontMotor.setSpeed(speedSetLeft);
  rightFrontMotor.setSpeed(speedSetRight);
  leftBackMotor.setSpeed(speedSetLeft);
}

void neg45(){
  leftFrontMotor.setSpeed(250);
  rightFrontMotor.setSpeed(250);
  leftBackMotor.setSpeed(250);
  leftFrontMotor.run(BACKWARD);
  rightFrontMotor.run(FORWARD);
  rightBackMotor.run(FORWARD);
  leftBackMotor.run(FORWARD);
  delay(300);
  leftFrontMotor.setSpeed(speedSetLeft);
  rightFrontMotor.setSpeed(speedSetRight);
  leftBackMotor.setSpeed(speedSetLeft);
}

void neg135(){
  leftFrontMotor.setSpeed(250);
  rightFrontMotor.setSpeed(250);
  leftBackMotor.setSpeed(250);
  leftFrontMotor.run(BACKWARD);
  rightFrontMotor.run(FORWARD);
  rightBackMotor.run(FORWARD);
  leftBackMotor.run(FORWARD);
  delay(900);
  leftFrontMotor.setSpeed(speedSetLeft);
  rightFrontMotor.setSpeed(speedSetRight);
  leftBackMotor.setSpeed(speedSetLeft);
}

void pos90(){
  leftFrontMotor.setSpeed(250);
  rightFrontMotor.setSpeed(250);
  leftBackMotor.setSpeed(250);
  leftFrontMotor.run(FORWARD);
  rightFrontMotor.run(BACKWARD);
  rightBackMotor.run(BACKWARD);
  leftBackMotor.run(BACKWARD);
  delay(480);
  leftFrontMotor.setSpeed(speedSetLeft);
  rightFrontMotor.setSpeed(speedSetRight);
  leftBackMotor.setSpeed(speedSetLeft);
}

void pos45(){
  leftFrontMotor.setSpeed(250);
  rightFrontMotor.setSpeed(250);
  leftBackMotor.setSpeed(250);
  leftFrontMotor.run(FORWARD);
  rightFrontMotor.run(BACKWARD);
  rightBackMotor.run(BACKWARD);
  leftBackMotor.run(BACKWARD);
  delay(240);
  leftFrontMotor.setSpeed(speedSetLeft);
  rightFrontMotor.setSpeed(speedSetRight);
  leftBackMotor.setSpeed(speedSetLeft);
}

void pos135(){
  leftFrontMotor.setSpeed(250);
  rightFrontMotor.setSpeed(250);
  leftBackMotor.setSpeed(250);
  leftFrontMotor.run(FORWARD);
  rightFrontMotor.run(BACKWARD);
  rightBackMotor.run(BACKWARD);
  leftBackMotor.run(BACKWARD);
  delay(705);
  leftFrontMotor.setSpeed(speedSetLeft);
  rightFrontMotor.setSpeed(speedSetRight);
  leftBackMotor.setSpeed(speedSetLeft);
}

void pos180(){
  pos90();
  moveStop(500);
  pos90();
}


void moveStop(int timeStop) {leftFrontMotor.run(RELEASE); rightFrontMotor.run(RELEASE); rightBackMotor.run(RELEASE); leftBackMotor.run(RELEASE); delay(timeStop);}

void moveForward(int multiplier) {
    leftFrontMotor.setSpeed(speedSetLeft);
    rightFrontMotor.setSpeed(speedSetRight);
    rightBackMotor.setSpeed(speedSetRight);
    leftBackMotor.setSpeed(speedSetLeft);
    leftFrontMotor.run(FORWARD);
    rightFrontMotor.run(FORWARD);
    rightBackMotor.run(FORWARD);
    leftBackMotor.run(BACKWARD);
    if (facing%2!=0){
      delay(multiplier*1500);
    }
    else{
      delay(multiplier*1000);
    }
}

long pingHead(){
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration/2) / 29.1;
  Serial.print(distance);
  Serial.println(" ");
  return distance;
}

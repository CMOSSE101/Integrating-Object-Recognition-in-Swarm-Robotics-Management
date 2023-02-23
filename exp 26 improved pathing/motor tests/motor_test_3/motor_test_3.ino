

int drive[] = {0,0,0,0,50}; // h bridge, delay




void setup() {
   // usb baudrate
  Serial.begin(9600);

  delay(1000); // delay for process to finish

  // set up motors
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
}

void updateMotor(int drive[]){
  if((drive[0] && drive[1]) || (drive[2] && drive[3])) { return;} // if mistake

  digitalWrite(3, drive[0]);
  digitalWrite(4, drive[1]);
  digitalWrite(5, drive[2]);
  digitalWrite(6, drive[3]);

  delay(drive[4]);
}


void turnRight(){
  for (int i=0; i<1; i++)
  {
    //             F B F B
    //int drive[] = {1,0,0,1,100};
    drive[0] = 1; drive[1] = 0; drive[2] = 0; drive[3] = 1; drive[4] = 850;
    updateMotor(drive); // turn robot
    delay(100);
    
    drive[0] = 0; drive[1] = 0; drive[2] = 0; drive[3] = 0;
    updateMotor(drive); // stop motors
    delay(100);
  }
}

void moveForwards(){
  
  // move forwards
  // B F B F
  drive[0] = 0; drive[1] = 1; drive[2] = 0; drive[3] = 1; drive[4] = 600;
  updateMotor(drive); // turn robot
  delay(100);
  
  // stop
  drive[0] = 0; drive[1] = 0; drive[2] = 0; drive[3] = 0;
  updateMotor(drive); // stop motors
  delay(100);
}


void loop() {
  delay(1000);
  moveForwards();

  
  delay(1000);
  turnRight();
}
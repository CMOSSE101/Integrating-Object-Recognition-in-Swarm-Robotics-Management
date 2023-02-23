

//
// https://www.youtube.com/watch?v=eoiuhPxCcM4&t=1643s
// Arduino with Python LESSON 17: Transferring Data over Ethernet UDP
//

// This verstion tries to drive robot forwards and right to clients command

#include <UIPEthernet.h>
//#include <Ethernet.h>

#include <Servo.h>

// crane/appendidge variables
Servo craneServo;
const int cranePin = 7;
int craneAngle = 90;
const int magnetPin = 2;
int action = 0; // 1 = GoTo, 2 = Pick up, 3 = Drop off

// network variables
const byte mac[] = {0x01,0x01,0x02,0x03,0x04,0x05};
IPAddress ip(192,168,0,201); // ip of device
const unsigned int localPort = 4031; // Chones port to comunicate over

// packet variables
char packetBuffer[24]; // message buffer of max size UDP_TX_PACKET_MAX_SIZE
String data; // to store buffer data in string format

char *command = NULL;
char* dataIn = "<Mode>[1,2]{Direction}(Type)<3>";
int packetSize;


// function prototypes
void dispSettings();
void getMode();
void moveNextGrid();

// System Settings
String mode = "X";
byte Xr = NULL;
byte Yr = NULL;
String Direction = "X";
String Type = "X";
byte ID = NULL;
byte Xd = NULL;
byte Yd = NULL;


// grid controll variables
//int movements[] = [];
int object_to_robot_global;
int currentDirection = 90;
int desiredDirection = 90;

// drive variables
int drive[] = {0,0,0,0,50}; // h bridge, delay

EthernetUDP Udp;

void motoDrive(int drive[]){
  if((drive[0] && drive[1]) || (drive[2] && drive[3])) { return;} // if mistake
  
  // pin values
  digitalWrite(3, drive[0]);
  digitalWrite(4, drive[1]);
  digitalWrite(5, drive[2]);
  digitalWrite(6, drive[3]);
  //Serial.println(drive[3]);
  // time delay
  delay(drive[4]);
}

void setup() {
  // usb baudrate
  Serial.begin(9600);
  // initialise ethenret using ip and mac adress
  Ethernet.begin(mac,ip);
  // inisitalise udp
  Udp.begin(localPort);

  delay(1000); // delay for process to finish
  Serial.println("IP :");
  Serial.println(ip);

  // set up motors
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  // set up buzzer
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);

  digitalWrite(3, LOW);
  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
  digitalWrite(6, LOW);

  digitalWrite(8, LOW);
  digitalWrite(9, LOW);

  // Display current values (check to see if blanked)
  dispSettings();

  // initialise crane servo
  craneServo.write(craneAngle);
  craneServo.attach(cranePin);
  // initialise electromagnet
  pinMode(magnetPin, OUTPUT);
  digitalWrite(magnetPin, LOW); // Turn off magnet
}


// moves crane to hight for save travel
void craneLift()
{
  // move arm -> loop until reached
  for (int pos = craneAngle; pos <= 110; pos +=1)
  {
    // move to position
    craneServo.write(craneAngle);
    // small delay
    delay(20);
    
    craneAngle = pos;
  }
}


// moves craen to hight for pickup
void craneDrop()
{
  // move arm -> loop until reached
  for (byte pos = craneAngle; pos >= 73; pos -= 1)
  {
    // move to position
    craneServo.write(craneAngle);
    // small delay
    delay(20);
    
    craneAngle = pos;
  }
}


void pickUp()
{
  digitalWrite(magnetPin, HIGH); // Energise magnet
  craneDrop(); // Drop arm to pickup hight
  delay(500);
  craneLift(); // lift to moving hight
  delay(1000);
}


void dropOff()
{
  craneDrop(); // Drop arm to pickup hight
  digitalWrite(magnetPin, LOW); // Energise magnet
  delay(500);
  craneLift(); // lift to moving hight
  delay(1000);
}


void getPacket(){
   packetSize = Udp.parsePacket(); // size of any incoming packets

  // check if request avaliable. If size > 0 then request present
  if(packetSize > 0)
  {
    Udp.read(packetBuffer, 24); // read message
    dataIn = packetBuffer; // convert data to string
    String dataStr(dataIn);
    Serial.println("Recived Command : " + dataStr);
    //command = strtok(dataIn, ":");

    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort()); // initialise a reply to client
    Udp.print("Recived Command : " + dataStr); // send reply message
    Udp.endPacket(); // reply ended

    // Get mode from message
    getMode();
  }
}


// Extracts string between to specified characters
String dataSplitter(char* dataTest, char endA, char endB)
{
  bool endAFound = false;
  bool endBFound = false;
  
  String Buff;
  for (int i=0; i<strlen(dataTest); i++)
  {
    // Check for end of segment
    if (dataTest[i] == endB){endBFound = true;}

    // Add character to the buffer
    if (endAFound and not(endBFound))
    {
      // Add character to the end 
      Buff = Buff + dataTest[i];
    }

    // Check for beginning of segment
    if (dataTest[i] == endA){endAFound = true;}
  }

  // Return extracted data
  return Buff;
}


// gets required coordinates for next movement
void gridControll(){
  Serial.println("GRID COMMAND");
  // Get new coordinates
  String coorSeg = dataSplitter(dataIn,'{','}');
  Xd = dataSplitter(dataIn,'{',',').toInt();
  Yd = dataSplitter(dataIn,',','}').toInt();
  action = dataSplitter(dataIn,'[',']').toInt();
  Serial.print("New Destination: ");Serial.print(Xd);Serial.print(",");Serial.println(Yd);

  // get robot to move there
  moveNextGrid();
}


void calcObjectRelation()
{
  // find placementr of robot (global direction)
  if (Yr < Yd) // if object above on Y axis
  {
      object_to_robot_global = 90; // Above
  }
  else if (Yr > Yd) // if object below on Y axis
  {
    object_to_robot_global = 270; // Bellow
  }
  else{
    if (Xr < Xd) // if object right on X axis
    {
        object_to_robot_global = 180; // Right
    }
    if (Xr > Xd) // if object left on X axis
    {
        object_to_robot_global = 0; // Left
    }
  }
  
  Serial.println("Object To Robot (Global) : ");
  Serial.println(object_to_robot_global);
}


void turnRight()
{

  Serial.println("Turning - Right");

  for (byte i=0; i<1; i++)
  {
    //             F B F B
    //int drive[] = {1,0,0,1,100};
    drive[0] = 1; drive[1] = 0; drive[2] = 0; drive[3] = 1; drive[4] = 850;
    motoDrive(drive); // turn robot
    delay(100);
    
    drive[0] = 0; drive[1] = 0; drive[2] = 0; drive[3] = 0;
    motoDrive(drive); // stop motors
    delay(100);
  }
  
  currentDirection = currentDirection + 90; // update direction 
}

void turnLeft()
{
  
  Serial.println("Turning - Right");
  
  for (byte i=0; i<1; i++)
  {
    //             F B F B
    //int drive[] = {0,1,1,0,100};
    drive[0] = 0; drive[1] = 1; drive[2] = 1; drive[3] = 0; drive[4] = 850;
    motoDrive(drive); // turn robot
    delay(100);
    
    drive[0] = 0; drive[1] = 0; drive[2] = 0; drive[3] = 0;
    motoDrive(drive); // stop motors
    delay(100);
  }
  
  currentDirection = currentDirection - 90; // update direction 
 
}

void moveForwards()
{
  Serial.println("Moving - Forwards");

  for (byte i=0; i<1; i++)
  {
    // move forwards
    // B F B F
    drive[0] = 0; drive[1] = 1; drive[2] = 0; drive[3] = 1; drive[4] = 600;
    motoDrive(drive); // turn robot
    delay(100);
  
    // stop
    drive[0] = 0; drive[1] = 0; drive[2] = 0; drive[3] = 0;
    motoDrive(drive); // stop motors
    delay(100);
  }
}


void rotateRobot()
{
  Serial.println("Calculating Robot Rotation");
  desiredDirection = object_to_robot_global;

  Serial.println("Current Direction: ");
  Serial.println(currentDirection);
  
  
  
  // correct rotation
  while(currentDirection != desiredDirection) // while rotation not at desired
  {
    Serial.println("CORRECTING ROTATION");
    
    if (currentDirection < desiredDirection) // if desires is more, turn clockwise
    {
        turnRight();
    }
    if (currentDirection > desiredDirection) // if desires is less, turn anti-clockwise
    {
        turnLeft(); 
    }

    // error correction
    if(currentDirection == 360)
    {
      currentDirection = 0;
    }
  }
}


void moveNextGrid(){

  //Serial.println("MOVING TO DEST");
  
  calcObjectRelation();

  // correct rotation
  if ((Xr!=Xd) ^ (Yr!=Yd)) // X-OR (make sure not at position already
  {
    rotateRobot();
  }

  // translateRobot
  // 1 = GoTo, 2 = Pick up, 3 = Drop off
  if (action == 1){
    // check not as destination
    //bool xDif = Xr!=Xd;
    //bool yDif = Yr!=Yd;
    if ((Xr!=Xd) ^ (Yr!=Yd)) // X-OR
    {
      //Serial.print("Robot Coordinates: ");Serial.print(Xr);Serial.print(",");Serial.println(Yr);
      //Serial.print("Dest Coordinates: ");Serial.print(Xd);Serial.print(",");Serial.println(Yd);
      moveForwards();
    }
  } else if (action == 2){
    pickUp();
  } else if (action == 3){
    dropOff();
  }

  // correct robot coordinates
  Xr = Xd;
  Yr = Yd;
  //currentDirection = desiredDirection;
}


// Initalisesand updates robot settings
void roboInit(){
  Serial.println("INITIALISING ROBOT SETTINGS");
  Serial.println(dataIn);
  // Gather segments form dataIn
  String IDSeg = dataSplitter(dataIn,'#','[');
  
  String coorSeg = dataSplitter(dataIn,'[',']');
  String dirSeg = dataSplitter(dataIn,'{','}');
  String typeSeg = dataSplitter(dataIn,'(',')');

  // Converting inputs to propper data types
  // ID
  ID = IDSeg.toInt();
  // Coordinates
  Xr = dataSplitter(dataIn,'[',',').toInt();
  Yr = dataSplitter(dataIn,',',']').toInt();

  // Update Robot Settings
  Direction = dirSeg;
  Type = typeSeg;
}


// gets the mode of the incomming message
void getMode(){
  //dataIn = "<0>#1[1,2]{N}(C)"; // test data
  //Serial.println(dataIn);

  // Extract the mode from the read message
  String modeSeg = dataSplitter(dataIn,'<','>');
  mode = modeSeg;
//  Serial.println("mode");Serial.println(mode);
//  Serial.println(mode == "0");

  // if valid mode was found
  if (mode != "")
  {
      mode = modeSeg; // Store into global 
    // Robogt initalise message detected
    if (mode == "0"){ 
      Serial.println("\n\nMessage Recieved - Robot Initialise");
      roboInit();
    }

    // Robot grid controll message detected
    if (mode == "3"){ 
      Serial.println("\n\nMessage Recieved - Grid Controll");
      gridControll();
    }

    delay(200);
    dispSettings();
    
  } else{
    // notify of invalid message
    Serial.println("\n\nMessage Recieved - INVALID");
  }

  
}

// Display settings values stored in meory
void dispSettings(){
  Serial.println("\n\nROBOT SETTINGS");
  Serial.print("Mode: ");Serial.println(mode);
  Serial.print("ID: ");Serial.println(ID);
  Serial.print("Robot Coordinates: ");Serial.print(Xr);Serial.print(",");Serial.println(Yr);
  Serial.print("Dest Coordinates: ");Serial.print(Xd);Serial.print(",");Serial.println(Yd);
  Serial.print("Direction: ");Serial.println(Direction);
  Serial.print("Robot Type: ");Serial.println(Type);
  delay(800);
}


// main loop
void loop(){
  
  // Turn of all motor
  //int drive[] = {0,0,0,0,200};
  drive[0] = 0; drive[1] = 0; drive[2] = 0; drive[3] = 0;
  motoDrive(drive);
  
  getPacket();

}



//void loop() {
//  // Turn of all motor
//  int drive[] = {0,0,0,0,200};
//  motoDrive(drive);
//
//  packetSize = Udp.parsePacket(); // size of any incoming packets
//
//  // check if request avaliable. If size > 0 then request present
//  if(packetSize > 0)
//  {
//    Udp.read(packetBuffer, 24); // read message
//    char data(packetBuffer); // convert data to string
//    Serial.println("Recived Command : " + data);
//    command = strtok(data, ":");
//    Serial.println("Recived Command : " + String(command[0]) + "-" + String(command[1]));
//    for(int i=0; i<atoi(command[1]); i++){
//      if (command[0] == "F") // If told to turn LED on
//        {
//          Udp.beginPacket(Udp.remoteIP(), Udp.remotePort()); // initialise a reply to client
//          Udp.print("Going - Forwards"); // send reply message
//          Udp.endPacket(); // reply ended
//    
//          Serial.println("forwards");
//          // forwards for 200 mill seconds
//          drive[1] = 1;
//          drive[3] = 1;
//          drive[4] = 500;
//        }
//    }
//    
//
//    if (data == "Right") // If told to turn LED on
//    {
//      Udp.beginPacket(Udp.remoteIP(), Udp.remotePort()); // initialise a reply to client
//      Udp.print("Going - Right"); // send reply message
//      Udp.endPacket(); // reply ended
//
//      Serial.println("right");
//      // right for 200 mill seconds
//      drive[1] = 1;
//      drive[2] = 1;
//      drive[4] = 300;
//    }
//
//    if (data == "Left") // If told to turn LED on
//    {
//      Udp.beginPacket(Udp.remoteIP(), Udp.remotePort()); // initialise a reply to client
//      Udp.print("Going - left"); // send reply message
//      Udp.endPacket(); // reply ended
//
//      Serial.println("left");
//      // right for 200 mill seconds
//      drive[0] = 1;
//      drive[3] = 1;
//      drive[4] = 300;
//    }
//
//    // drive motor
//    motoDrive(drive);
//    
//    // clear packet buffer
//    memset(packetBuffer, 0, 24);
//    
//  } // end - packet size
//  
//} // end - loop

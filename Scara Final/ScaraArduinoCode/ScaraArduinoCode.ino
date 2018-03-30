// Serial test script

#include <Servo.h>

#define EAA 1
#define EAB 2
 
int cntEA = 0;
bool curEA = LOW;
bool lasEA = LOW;
 
Servo myservoj1;  // create servo object to control a servo
Servo myservoj2;  // create servo object to control a servo

 
int pos = 90;    // variable to store the servo position
 

int setPoint = 55;
String readString="";
int x =5 ;

void setup()
{
  pinMode (EAA, INPUT);
  pinMode (EAB, INPUT);
  Serial.begin(9600);  // initialize serial communications at 9600 bps
    myservoj1.attach(9); //Servo connected to D9
    myservoj2.attach(10); //Servo connected to D10
}
void loop()
{


//  while (Serial.available() > 0) {
//                // read the incoming byte:
//                 int c = Serial.read();
//                 Serial.println(c);
//                 char x = Serial.read();
//                 Serial.println(x);
//                delay(2); 
//                // say what you got:
//                //Serial.print("C is ");
//                Serial.println(c, DEC);
//                myservoj1.write(c);
                ///////////////////////////////////////////////////
  // serial read section


  lasEA = curEA;
  while (Serial.available()) // this will be skipped if no data present, leading to
                             // the code sitting in the delay function below
  {

    delay(30);  //delay to allow buffer to fill 
    if (Serial.available() >0)
    {
      char c = Serial.read();  //gets one byte from serial buffer
      readString += c; //makes the string readString
      Serial.println(readString); //##### see what my input is 
    }
  }
  
  if (readString.length() ==4)
  { 
    if (readString ="K000")
    {
//      break
        Serial.print("Killing Code");

    }
    String  ard_sends = "a666";
  //Serial.print("Arduino sends: ");
    Serial.println(ard_sends);
    delayMicroseconds(500);
//  Serial.print("\n");
    ard_sends = "b999";
  //Serial.print("Arduino sends: ");
    Serial.println(ard_sends);
//  Serial.print("\n");
    
    
    readString="";
    //Serial.print("\n");
    Serial.flush();
  }

  //delay(500);

  // serial write section
  //read    
//  Serial.write("A444") 
//String  ard_sends = "C100";

//  Serial.println(ard_sends);
//
//  ard_sends = "D201";
//
//  Serial.println(ard_sends);
//
//
//  ard_sends = "E302";
//
//  Serial.println(ard_sends);
//
//  delay(500);
//  
  //Serial.flush();
  //x=x+1;
  //if  (x>9 )
  //{
  //for (;;);
  //}
  
}

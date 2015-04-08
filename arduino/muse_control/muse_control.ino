int FORWARD = 2;
int BACKWARD = 4;
int LEFT = 8;
int RIGHT = 12;

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false, goodString = false;  // whether the string is complete
int forward=HIGH, backward=HIGH, left=HIGH, right=HIGH;

void setup() {
  // initialize serial:
  Serial.begin(115200);
  // reserve 200 bytes for the inputString:
  inputString.reserve(100);
  pinMode(FORWARD, OUTPUT);
  pinMode(BACKWARD, OUTPUT);
  pinMode(LEFT, OUTPUT);
  pinMode(RIGHT, OUTPUT);
  pinMode(13, OUTPUT);
  
  digitalWrite(FORWARD, HIGH);
  digitalWrite(BACKWARD, HIGH);
  digitalWrite(LEFT, HIGH);
  digitalWrite(RIGHT, HIGH);
}

void loop() {

  if (stringComplete) {
//    Serial.println(inputString);
    
    goodString = false;
    
    if(inputString == "F\n"){
      digitalWrite(13, HIGH);
      forward = LOW;
      backward = HIGH;
      goodString = true;
    }
    else if(inputString == "B\n"){
      forward = HIGH;
      backward = LOW;
      goodString = true;
    }
    else if(inputString == "L\n"){
      left = LOW;
      right = HIGH;
      goodString = true;
    }
    else if(inputString == "R\n"){
      left = HIGH;
      right = LOW;
      goodString = true;
    }
    else if(inputString == "S\n"){
      digitalWrite(13, LOW);
      left = HIGH;
      right = HIGH;
      forward = HIGH;
      backward = HIGH;
      goodString = true;
    }
    else{
      goodString = false;
    }
    
    if(goodString){
      digitalWrite(FORWARD, forward);
      digitalWrite(BACKWARD, backward);
      digitalWrite(LEFT, left);
      digitalWrite(RIGHT, right);
    Serial.print('!');
    }
      
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
}

/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read(); 
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    } 
  }
}


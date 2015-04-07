int F = 2;
int B = 4;
int L = 8;
int R = 12;
int light = 13;
int left, right, forward, backward;
boolean goodString = false;
char command = 'k';

void setup() {
  // put your setup code here, to run once:
//  Serial.begin(9600);
  Serial.begin(115200);
  pinMode(F, OUTPUT);
  pinMode(B, OUTPUT);
  pinMode(L, OUTPUT);
  pinMode(R, OUTPUT);
  pinMode(light, OUTPUT);
}

void loop() {
   
      forward = HIGH;
      backward = LOW;
      left = LOW;
      right = LOW;
      if(command == 'd'){
        Serial.println("Move forward");
        forward = HIGH;
        backward = LOW;
        goodString = true;
      }
      else if(command == 's'){
        Serial.println("Move backward");
        forward = LOW;
        backward = HIGH;
        goodString = true;
      }
      else if(command == 'a'){
        Serial.println("Move left");
        left = HIGH;
        right = LOW;
        goodString = true;
      }
      else if(command == 'f'){
        Serial.println("Move right");
        left = LOW;
        right = HIGH;
        goodString = true;
      }
      else if(command == 'x'){
        Serial.println("stop!");
        digitalWrite(light, LOW);
        left = LOW;
        right = LOW;
        forward = LOW;
        backward = LOW;
        goodString = true;
      }
      else{
        goodString = false;
      }
      
      if(goodString){
        digitalWrite(F, forward);
        digitalWrite(B, backward);
        digitalWrite(L, left);
        digitalWrite(R, right);
        delay(1000);
      }
      command = 'k';
   
}

void serialEvent() {
  while (Serial.available()) {
//    Serial.println("getting next command");
    // get the new byte:
//    char nextCommand = (char)Serial.read(); 
    // add it to the inputString:
    command = Serial.read();
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
  }
}

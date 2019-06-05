// Left Motor (A)
int enA = 3;
int in1 = 9;
int in2 = 8;
// Right Motor (B)
int enB = 5;
int in3 = 7;
int in4 = 6;
int sp = 100;
int len = 500;
int inByte = 0 ;

void setup()
{
  // Declare motor control pins to be in output
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  Serial.begin(9600);
  //while (!Serial) {
  // ; // wait for serial port to connect. Needed for native USB port only
  //}
  Serial.write("STEVE-0.1");
}

/*  Move forward function
    Dir (Boolean) { true: Forward,
          false: Backward }
    Spd (Int) { 0 <-> 255 }
    Dur (Int) { Duration (in ms) }
*/

void moveBot(bool dir, int spd, int dur) {
  // Motor A
  digitalWrite(in1, dir);
  digitalWrite(in2, !dir);  //The '!' symbol inverts the boolean value. So for example, if dir is true, !dir is false.
  // Motor B
  digitalWrite(in3, dir);
  digitalWrite(in4, !dir);
  // Set motor speed to spd
  analogWrite(enA, spd);
  analogWrite(enB, spd);
  //Motion Duration
  delay(dur);
}

/*  Rotate function
    Dir (Boolean) { true: Clockwise,
          false: Anti-clockwise }
    Spd (Int) { 0 <-> 255 }
    Dur (Int) { Duration (in ms) }
*/

void rotateBot(bool dir, int spd, int dur) {
  // Motor A
  digitalWrite(in1, dir);
  digitalWrite(in2, !dir);  //The '!' symbol inverts the boolean value. So for example, if dir is true, !dir is false.
  // Motor B
  digitalWrite(in3, !dir);
  digitalWrite(in4, dir);
  // Set motor speed to spd
  analogWrite(enA, spd);
  analogWrite(enB, spd);
  //Rotation Duration
  delay(dur);
}

//Turn off both motors
void stopMotors() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

void loop()
{
  // Move forward for 2s @ speed 200
  //moveBot(true, sp, 1000);

  //stopMotors();
  // Rotate bot for 1s clockwise @ speed 150
  //rotateBot(true, sp, 1000);
  // Move backward for 2s @ speed 200
  //moveBot(false, sp, 1000);
  // Rotate bot for 1s anti-clockwise @ speed 150
  //rotateBot(false, sp, 1000);
  // Stop motors for 1s @ speed 200
  //moveBot(false, sp, 1000);
  //stopMotors();
  if (Serial.available() > 0) {
    // get incoming byte:
    inByte = Serial.read();
    switch (inByte){
      case ']':
        sp = sp + 10;
        break;
      case '[':
        sp = sp - 10;
        break;
      case '}':
        len = len + 50;
        break;
      case '{':
        len = len - 50;
        break;
      case 'w':
        moveBot(true,sp,len);
        stopMotors();
        break;
      case 's':
        moveBot(false,sp,len);
        stopMotors();
        break;
      case 'a':
        rotateBot(false,sp,len);
        stopMotors();
        break;
      case 'd':
        rotateBot(true,sp,len);
        stopMotors();
        break;

    }
  }
}

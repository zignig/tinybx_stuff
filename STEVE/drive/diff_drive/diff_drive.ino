// Left Motor (A)
int enA = 3;
int in1 = 9;
int in2 = 8;
// Right Motor (B)
int enB = 5;
int in3 = 7;
int in4 = 6;
int sp = 150;

void setup()
{
  // Declare motor control pins to be in output
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  // A 2s delay before starting main loop
  // The LED at pin 13 will turn on for ~2s to indicate delay
  digitalWrite(13, HIGH);
  delay(1900);
  digitalWrite(13, LOW);
  delay(100);

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
  moveBot(true, sp, 1000);

  //stopMotors();
  // Rotate bot for 1s clockwise @ speed 150
  rotateBot(true, sp, 1000);
  // Move backward for 2s @ speed 200
  moveBot(false, sp, 1000);
  // Rotate bot for 1s anti-clockwise @ speed 150
  rotateBot(false, sp, 1000);
  // Stop motors for 1s @ speed 200
  moveBot(false, sp, 1000);
  stopMotors();
  delay(1000);
}

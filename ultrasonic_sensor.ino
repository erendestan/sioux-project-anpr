const int trigPin1 = 8;
const int echoPin1 = 9;

const int trigPin2 = 11;
const int echoPin2 = 10;

const int redPin = 13;
const int greenPin = 12;


void setup() {
  Serial.begin(9600);
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);

  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);

  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
}


void loop() {
  int distance1 = measureDistance(trigPin1, echoPin1);
  int distance2 = measureDistance(trigPin2, echoPin2);

  // Serial.print(distance1);
  // Serial.print(",");
  // Serial.println(distance2);
  Serial.println(getParkingStatus(distance1, distance2));
  // Serial.println();

  delay(1000);  // Adjust the delay as needed
}

int measureDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  unsigned long duration = pulseIn(echoPin, HIGH);
  return duration * 0.034 / 2;
}

int getParkingStatus(int distance1, int distance2) {
  if (distance1 <= 15 && distance2 <= 15) {
    // Both spaces are taken
    digitalWrite(redPin, HIGH);
    digitalWrite(greenPin, LOW);
    return 3;  // '3' to Python script indicating "Both Taken"
  } else if (distance1 <= 15) {
    // Space 1 is taken
    digitalWrite(redPin, LOW);
    digitalWrite(greenPin, HIGH);
    return 2;  // '2' to Python script indicating "First space is taken"
  } else if (distance2 <= 15) {
    // Space 2 is taken
    digitalWrite(redPin, LOW);
    digitalWrite(greenPin, HIGH);
    return 1;  // '1' to Python script indicating "Second space is taken"
  } else {
    // Neither space is taken
    digitalWrite(redPin, LOW);
    digitalWrite(greenPin, HIGH);
    return 0;  // '0' to Python script indicating "None Taken"
  }
}

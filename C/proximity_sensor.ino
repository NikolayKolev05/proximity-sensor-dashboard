#include <LiquidCrystal.h>

LiquidCrystal lcd(4, 5, 9, 10, 11, 12);

const int trigPin = 3;
const int echoPin = 2;
const int ledPinRed = 6;
const int buzzer = 7;
const int ledPinGreen=8;
const int ledPinYellow=13;

void setup() {
  pinMode(buzzer, OUTPUT);
  pinMode(ledPinRed, OUTPUT);
  pinMode(ledPinGreen,OUTPUT);
  pinMode(ledPinYellow,OUTPUT);
  lcd.begin(16, 2);
  delay(100);
  lcd.print("Distance: ");
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000);
  int distance = duration * 0.034 / 2;

  lcd.setCursor(10, 0);
  if (distance < 0 || distance > 500) {
    lcd.print("ERR ");
  } else {
    lcd.print("    ");
    lcd.setCursor(10, 0);
    lcd.print(distance);
    lcd.print("cm ");
    Serial.println(distance);
  }
  if (distance <20)
  {
    digitalWrite(ledPinGreen,HIGH);
  }
  if (distance > 20) {
    digitalWrite(ledPinRed, HIGH);
    noTone(buzzer);
  } else {
    digitalWrite(ledPinRed, LOW);
    tone(buzzer, 1000);
  }
  
  delay(500);
}
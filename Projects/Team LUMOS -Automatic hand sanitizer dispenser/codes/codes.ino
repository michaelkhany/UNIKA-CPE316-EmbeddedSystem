#include <LiquidCrystal.h>
#define SIGNAL_PIN 33 
#define RELAY_PIN 21 

const int rs = 22, en = 4, d4 = 15, d5 = 13, d6 = 26, d7 = 21;

LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

const int trigPin = 5;

const int echoPin = 18;

long duration;

int distance; 

int value = 0; 



void setup() {

  Serial.begin(9600);

  delay(2000);
  
  pinMode(trigPin, OUTPUT);

  pinMode(echoPin, INPUT);

  pinMode(RELAY_PIN, OUTPUT);

  digitalWrite(RELAY_PIN, LOW); 

  ledcSetup(0,1E5,12);
  ledcAttachPin(32,0);
  
  lcd.begin(16, 2);

  lcd.clear();

  lcd.setCursor(0,0);

  lcd.print("Covid19 Tracker");

  lcd.setCursor(0,1);

  lcd.print("Hand Sanitizer");
}

void ultra(){

  digitalWrite(trigPin, LOW);

  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);

  delayMicroseconds(10);

  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);

  distance = duration * 0.0340 / 2;

  Serial.println("Distance");

  Serial.println(distance);

  digitalWrite(RELAY_PIN, HIGH);  // turn the sensor ON
  delay(10);                      // wait 10 milliseconds
  value = analogRead(SIGNAL_PIN); // read the analog value from sensor
  digitalWrite(RELAY_PIN, LOW);   // turn the sensor OFF
  

  if (distance > 1 && distance <= 15){
     ledcWriteTone(0,800);
    delay(2000);
    uint8_t octave = 1;
    ledcWriteNote(0,NOTE_C,octave);  
    delay(2000);
    ledcWriteTone(0,0);
    
    Serial.print("Opening Pump");
    digitalWrite(RELAY_PIN, HIGH); // turn on pump 4 seconds
    delay(4000);
    digitalWrite(RELAY_PIN, LOW);  // turn off pump 4 seconds
    delay(4000);
  
    }
    Serial.print("The water sensor value: ");
    Serial.println(value);

    if ( value <= 300){
      ledcWriteTone(0,800);
      delay(1000);
      uint8_t octave = 1;
      ledcWriteNote(0,NOTE_C,octave);  
      delay(1000);
      ledcWriteTone(0,0);
    }

}

void loop() {

  ultra();
  
  digitalWrite(RELAY_PIN, LOW); 

}

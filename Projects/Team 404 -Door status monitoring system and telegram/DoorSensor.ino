
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <UniversalTelegramBot.h>
#include <ArduinoJson.h>

// Set GPIOs for LED and reedswitch
const int reedSwitch = 4;
const int led = 2; //optional

// Detects whenever the door changed state
bool changeState = false;

// Holds reedswitch state (1=opened, 0=close)
bool state;
String doorState;

// Auxiliary variables (it will only detect changes that are 1500 milliseconds apart)
unsigned long previousMillis = 0; 
const long interval = 1500;

const char* ssid = "S8 plus";
const char* password = "123456789";

// Initialize Telegram BOT
#define BOTtoken "5384542786:AAHXm2q-CoZoX09FZ1FYVmd3efXLphojDW8"  // your Bot Token (Get from Botfather)

// Use @myidbot to find out the chat ID of an individual or a group
// Also note that you need to click "start" on a bot before it can
// message you
#define CHAT_ID "781006061"

WiFiClientSecure client;
UniversalTelegramBot bot(BOTtoken, client);

// Runs whenever the reedswitch changes state
ICACHE_RAM_ATTR void changeDoorStatus() {
  Serial.println("State changed");
  changeState = true;
}




void setup() {
  // Serial port for debugging purposes
  Serial.begin(115200);  

  // Read the current door state
  pinMode(reedSwitch, INPUT_PULLUP);
  state = digitalRead(reedSwitch);

  // Set LED state to match door state
  pinMode(led, OUTPUT);
  digitalWrite(led, !state);
  
  // Set the reedswitch pin as interrupt, assign interrupt function and set CHANGE mode
  attachInterrupt(digitalPinToInterrupt(reedSwitch), changeDoorStatus, CHANGE);

  // Connect to Wi-Fi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  client.setCACert(TELEGRAM_CERTIFICATE_ROOT); // Add root certificate for api.telegram.org
  while (WiFi.status() != WL_CONNECTED ) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected"); 
   bot.sendMessage(CHAT_ID, "Bot started up", "");
}
   
  unsigned long check_wifi = 600000;
void loop ()
{
  // if wifi is down, try reconnecting every 30 seconds
  if ((WiFi.status() != WL_CONNECTED) && (millis() > check_wifi)) 
  {
    Serial.println("Reconnecting to WiFi...");
    WiFi.disconnect();
    WiFi.begin(ssid, password);
    check_wifi = millis() + 600000;
  } 
   if (changeState){
    unsigned long currentMillis = millis();
    if(currentMillis - previousMillis >= interval) {
      previousMillis = currentMillis;
      // If a state has occured, invert the current door state   
        state = !state;
        if(state) {
          doorState = "closed";
        }
        else{
          doorState = "open";
        }
        digitalWrite(led, !state);
        changeState = false;
        Serial.println(state);
        Serial.println(doorState);
        
        //Send notification
        bot.sendMessage(CHAT_ID, "The door is " + doorState, "");
    }  
  }
}


 


/*void loop() {
  if (changeState){
    unsigned long currentMillis = millis();
    if(currentMillis - previousMillis >= interval) {
      previousMillis = currentMillis;
      // If a state has occured, invert the current door state   
        state = !state;
        if(state) {
          doorState = "closed";
        }
        else{
          doorState = "open";
        }
        digitalWrite(led, !state);
        changeState = false;
        Serial.println(state);
        Serial.println(doorState);
        
        //Send notification
        bot.sendMessage(CHAT_ID, "The door is " + doorState, "");
    }  
  }
}*/

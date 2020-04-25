/*
  Connection:

  WS2812B:
  D4

  Buzzer:
  D0


*/

#include <SPI.h>
#include <Adafruit_NeoPixel.h>

#define LED_PIN 2
#define REDCOLOR led.Color(20, 0, 0)
#define GREENCOLOR led.Color(0, 20, 0)
#define BLUECOLOR led.Color(0, 0, 20)
#define YELLOWCOLOR led.Color(10, 10, 0)
#define WHITECOLOR led.Color(10, 10, 10)
#define BLACKCOLOR led.Color(0, 0 ,0)

#define BUZZPIN 16


String name = "dev2";

Adafruit_NeoPixel led = Adafruit_NeoPixel(8, LED_PIN, NEO_GRB + NEO_KHZ800);


void setup() {
  led.begin();
  led.setPixelColor(0, YELLOWCOLOR);
  led.show();

  Serial.begin(9600);

  led.setPixelColor(0, BLUECOLOR);
  led.show();

  pinMode(BUZZPIN, OUTPUT);
  digitalWrite(BUZZPIN, HIGH);
}

void loop() {
  
  if ( Serial.available() > 0 )
  {
    String rec = Serial.readStringUntil('\n');
    if ( rec == "getName" )
      Serial.println(name);
    else if ( rec == "startAlarm" )
    {
      digitalWrite(BUZZPIN, LOW);
      for (int i = 0; i < 8; i++)
        led.setPixelColor(i, REDCOLOR);
      led.show();
      Serial.println("Alarm started");
    }
    else if ( rec == "soundSignal" )
    {
      digitalWrite(BUZZPIN, LOW);
      delay(20);
      digitalWrite(BUZZPIN, HIGH);
      Serial.println("Signal emitted");
    }
    else if ( rec == "doubleSoundSignal" )
    {
      digitalWrite(BUZZPIN, LOW);
      delay(20);
      digitalWrite(BUZZPIN, HIGH);
      delay(100);
      digitalWrite(BUZZPIN, LOW);
      delay(20);
      digitalWrite(BUZZPIN, HIGH);
      Serial.println("Signal emitted");
    }
    else if ( rec == "stopAlarm" )
    {
      digitalWrite(BUZZPIN, HIGH);
      for (int i = 0; i < 8; i++)
        led.setPixelColor(i, BLUECOLOR);
      led.show();
      Serial.println("Alarm stopped");
    }
    else if ( rec == "LEDgreen" )
    {
      for (int i = 0; i < 8; i++)
        led.setPixelColor(i, GREENCOLOR);
      led.show();
      Serial.println("Showed green color");
    }
    else if ( rec == "LEDred" )
    {
      for (int i = 0; i < 8; i++)
        led.setPixelColor(i, REDCOLOR);
      led.show();
      Serial.println("Showed red color");
    }
    else if ( rec == "LEDblue" )
    {
      for (int i = 0; i < 8; i++)
        led.setPixelColor(i, BLUECOLOR);
      led.show();
      Serial.println("Showed blue color");
    }
    else if ( rec == "LEDyellow" )
    {
      for (int i = 0; i < 8; i++)
        led.setPixelColor(i, YELLOWCOLOR);
      led.show();
      Serial.println("Showed yellow color");
    }
    else if ( rec == "LEDblack" || rec == "turnOffLED" )
    {
      for (int i = 0; i < 8; i++)
        led.setPixelColor(i, BLACKCOLOR);
      led.show();
      Serial.println("Turned off LEDs");
    }
    else if ( rec == "LEDwhite" || rec == "turnOnLED" )
    {
      for (int i = 0; i < 8; i++)
        led.setPixelColor(i, WHITECOLOR);
      led.show();
      Serial.println("Turned on LEDs");
    }
    else if ( rec == "sendservices" )
    {
      Serial.println("startAlarm;soundSignal;doubleSoundSignal;stopAlarm;LEDgreen;LEDred;LEDblue;LEDyellow;LEDblack;LEDwhite");
    }
    else
      Serial.println(rec);
  }
}

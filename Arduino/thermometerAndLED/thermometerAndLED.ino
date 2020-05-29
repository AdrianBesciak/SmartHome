#include <OneWire.h>
#include <DallasTemperature.h>

String name = "dev1";

#define thermometerPin 2
#define LEDPin 3
 
OneWire oneWire(thermometerPin); //Podłączenie do A5
DallasTemperature sensors(&oneWire); //Przekazania informacji do biblioteki
 
void setup(void) {
  pinMode(LEDPin, OUTPUT);
  digitalWrite(LEDPin, LOW);
  Serial.begin(9600);
  sensors.begin(); //Inicjalizacja czujnikow
}


void send(String com) {
  com = com + "}";
  Serial.println(com);
}
 
void loop(void) {

  if ( Serial.available() > 0 )
  {
    String rec = Serial.readStringUntil('\n');
    if ( rec == "getName" )
      send(name);
    else if ( rec == "getTemperature" )
    {
      sensors.requestTemperatures(); //Pobranie temperatury czujnika
      String msg = "Temperature: ";
      msg = msg + sensors.getTempCByIndex(0);
      send(msg);  //Wyswietlenie informacji
    }
    else if (rec == "turnOnLED")
    {
      digitalWrite(LEDPin, HIGH);
      send("LEDTurnedOn");
    }
    else if (rec == "turnOffLED")
    {
      digitalWrite(LEDPin, LOW);
      send("LEDTurnedOff");
    }
    else if (rec == "toggleLED")
    {
      if (digitalRead(LEDPin))
      {
        digitalWrite(LEDPin, LOW);
        send("LEDTurnedOff");        
      }
      else
      {
        digitalWrite(LEDPin, HIGH);
        send("LEDTurnedOn");
      }
    }
    else if (rec == "sendservices")
    {
      send("getTemperature;turnOnLED;turnOffLED;toggleLED");
    }
    else
      send(rec);
  }
  
}

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
 
void loop(void) {

  if ( Serial.available() > 0 )
  {
    String rec = Serial.readStringUntil('\n');
    if ( rec == "getName" )
      Serial.println(name);
    else if ( rec == "getTemperature" )
    {
      sensors.requestTemperatures(); //Pobranie temperatury czujnika
      Serial.println(sensors.getTempCByIndex(0));  //Wyswietlenie informacji
    }
    else if (rec == "turnOnLED")
    {
      digitalWrite(LEDPin, HIGH);
      Serial.println("LEDTurnedOn");
    }
    else if (rec == "turnOffLED")
    {
      digitalWrite(LEDPin, LOW);
      Serial.println("LEDTurnedOff");
    }
    else if (rec == "sendservices")
    {
      Serial.println("getTemperature;turnOnLED;turnOffLED");
    }
    else
      Serial.println(rec);
  }
  
}

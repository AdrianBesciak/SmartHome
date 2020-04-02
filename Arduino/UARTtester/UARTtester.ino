String name;


void setup()
{
  Serial.begin(9600);
  while(!Serial)
  {
    ;
  }
  name = "Urzadzenie 1";
}

void loop() // run over and over
{
  if ( Serial.available() > 0 )
  {
    String rec = Serial.readStringUntil('\n');
    if ( rec == "getname" )
      Serial.println(name);
    else
      Serial.println(rec);
  }
    
}

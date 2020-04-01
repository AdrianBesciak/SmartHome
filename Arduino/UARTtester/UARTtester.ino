
void setup()
{
  Serial.begin(9600);
  while(!Serial)
  {
    ;
  }
}

void loop() // run over and over
{
  if ( Serial.available() > 0 )
    Serial.println(Serial.readStringUntil('\n'));
}

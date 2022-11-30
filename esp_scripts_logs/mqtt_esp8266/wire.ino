uint8_t pcf8574_addr=0x20; // PCF8574P

void dxRead(){
  Wire.requestFrom (pcf8574_addr,1); 
  if (Wire.available ()) {
    uint8_t rv;
    rv=Wire.read();
    for(uint8_t i=0;i<=7;i++){ DXr[i]=bitRead(rv, i); }
  }
  Wire.requestFrom (pcf8574_addr+1,1); 
  if (Wire.available ()) {
    uint8_t rv;
    rv=Wire.read();
    for(uint8_t i=0;i<=7;i++){ DXr[i+8]=bitRead(rv, i); }
  }
}

void dxWrite(){
  uint8_t data=0xFF;
  for(uint8_t i=0;i<=7;i++){    if(DXw[i]==0) bitClear(data, i);  }
  Wire.beginTransmission (pcf8574_addr);
  Wire.write(data); Wire.endTransmission ();
  data=0xFF;
  for(uint8_t i=0;i<=7;i++){    if(DXw[i+8]==0) bitClear(data, i);  }
  Wire.beginTransmission (pcf8574_addr+1);
  Wire.write(data); Wire.endTransmission ();
  
  //Serial.println(DXw[0]);
  delay(10);
}


// ---------------------------------------------------------------- //
// Arduino Ultrasoninc Sensor HC-SR04
// Re-writed by Arbi Abdul Jabbaar
// Using Arduino IDE 1.8.7
// Using HC-SR04 Module
// Tested on 17 September 2019
// ---------------------------------------------------------------- //

#include <Wire.h> //Needed for I2C to GNSS

#include <SparkFun_u-blox_GNSS_Arduino_Library.h> //http://librarymanager/All#SparkFun_u-blox_GNSS
SFE_UBLOX_GNSS myGNSS;

long lasttime = 0;
int count = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial)
    ; //Wait for user to open terminal
  Serial.println("SparkFun u-blox Example");

  Wire.begin();

  if (myGNSS.begin() == false) //Connect to the u-blox module using Wire port
  {
    Serial.println(F("u-blox GNSS not detected at default I2C address. Please check wiring. Freezing."));
    while (1)
      ;
  }

  myGNSS.setI2COutput(COM_TYPE_UBX); //Set the I2C port to output UBX only (turn off NMEA noise)
  //myGNSS.saveConfiguration();        //Optional: Save the current settings to flash and BBR
}


void loop() {
  if(millis()-lasttime>=1000){ //read data every second
    count++;
    lasttime = millis();
    readData();
  }

  if(count==100){
    Serial.print("Finished. 100 data points are acquired. Format=<LATITUDE,LONGITUDE> *10^-7");
    while(1);
  }
}

void readData(){
    long latitude = myGNSS.getLatitude();
    Serial.print(latitude);

    long longitude = myGNSS.getLongitude();
    Serial.print(F(" "));
    Serial.print(longitude);
    Serial.println();
}
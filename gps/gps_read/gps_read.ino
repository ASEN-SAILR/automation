
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
    readData();
    count++;
    lasttime = millis(); 
  }

  if(count==100){
    Serial.print("Finished. 100 data points are acquired. Format=<LATITUDE*10^-7 LONGITUDE*10^-7 ALTITUDE>");
    while(1);
  }
}

void readData(){

    /*0 = no fix
    1 = dead reckoning (requires external sensors)
    2 = 2D (not quite enough satellites in view)
    3 = 3D (the standard fix)
    4 = GNSS + dead reckoning (requires external sensors)
    5 = Time fix only*/
    byte fixType = myGNSS.getFixType();
    long lastfix = millis();
    while(fixType!=3){
      if(millis()-lasttime>=1000){
        Serial.print("Fix type:");
        Serial.print(fixType);
        Serial.print(" Waiting for 3D fix...");
        Serial.println();
        lasttime = millis();
      }
    }
    
    long latitude = myGNSS.getLatitude();
    Serial.print(latitude);

    long longitude = myGNSS.getLongitude();
    Serial.print(F(" "));
    Serial.print(longitude);

    long altitude = myGNSS.getAltitude();
    Serial.print(F(" "));
    Serial.print(altitude);

    Serial.println();
}
#include <veml6040.h>

/*
The MIT License (MIT)
Copyright (c) 2015 thewknd
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

#include "Wire.h"
#include "veml6040.h"
#include "veml6040_2.h"
#include "SparkFun_SGP30_Arduino_Library.h" 

// SGP30 mySensor;
VEML6040 pHSensor;
// VEML6040_2 drinkSensor;


byte bitConvert(uint16_t valueRGB)
{
  float scaledRGB = (float)(valueRGB/(65535.0))*255.0;
  byte scaledRGB_byte = (byte)scaledRGB;
  return scaledRGB_byte; 
}






// pH to RGB Using Color Picker Tool Online
// Hue values can be used to 
// pH 1 = rgb(186,58,55) - Hue 1
// pH 2 = rgb(225,75,77) - Hue 359
// pH 3 = rgb(249,146,67) - Hue 26
// pH 4 = rgb(236,143,37) - Hue 32
// pH 5 = rgb(244,173,19) - Hue 41
// pH 6 = rgb(244,249,22) - Hue 61
// pH 7 = rgb(254,212,100) - Hue 44
// pH 8 = rgb(200,169,102) - Hue 41
// pH 9 = rgb(111,98,63) - Hue 44
// pH 10 = rgb(98,88,76) - Hue 33
// pH 11 = rgb(73,70,127)
// pH 12 = rgb(67,46,65)
// pH 13 = rgb(48,31,50)
// pH 14 = rgb(62,31,37)

// Define RGB and pH data
// const byte red[] = {186, 225, 249, 236, 244, 244, 254, 200, 111, 98, 73, 67, 48, 62};
// const byte green[] = {58, 75, 146, 143, 173, 249, 212, 169, 98, 88, 70, 46, 31, 31};
// const byte blue[] = {55, 77, 67, 37, 19, 22, 100, 102, 63, 76, 127, 65, 50, 37};

byte rgbValues[4][3] = {
  // {186,58, 55},
  {225,75,77},
  {249,146, 67},
  {236, 143, 37},
  {244, 173, 19},
  // {244, 249, 22},
  // {254, 212, 100},
  // {200, 169, 102},
  // {111, 98, 63},
  // {98,88,76},
  // {73, 70, 127},
  // {67, 46, 65},
  // {48, 31, 50},
  // {62, 31, 37}
};

float Hue, Saturation, Value;

const float pHValues[4] = {2.0,3.0,4.0,5.0};

float convertRGBtoPH(int r, int g, int b) {
  for (int i = 0; i < 3; i++) {
    if (r == rgbValues[i][0] && g == rgbValues[i][1] && b == rgbValues[i][2]) {
      return pHValues[i];
    }
    else if (r > rgbValues[i][0] && r < rgbValues[i+1][0] && g > rgbValues[i][1] && g < rgbValues[i+1][1] && b > rgbValues[i][2] && b < rgbValues[i+1][2]) {
      float pH = pHValues[i] + ((pHValues[i+1] - pHValues[i]) / (rgbValues[i+1][0] - rgbValues[i][0])) * (r - rgbValues[i][0]);
      return pH;
    }
  }
  // If the RGB values do not match any calibration data points, return -1
  return -1;
}

void rgbToHsv(byte r, byte g, byte b, float &h, float &s, float &v)
{
  float red = float(r) / 255.0;
  float green = float(g) / 255.0;
  float blue = float(b) / 255.0;

  float cmax = max(max(red,green), blue);
  float cmin = min(min(red,green), blue);
  float delta = cmax - cmin;

  if (delta == 0)
  {
    h = 0;
  }
  else if (cmax == red)
  {
    h = fmod((green-blue) / delta, 6.0);
  }
  else if (cmax == green)
  {
    h = ((blue - red) / delta) + 2;
  }
  else
  {
    h = ((red-green) / delta) + 4;
  }
h = h*60;
if  (h < 0)
{
  h += 360;
}
  s = (cmax ==0) ? 0 : delta / cmax;
  v = cmax;
}


void setup() {
  Serial.begin(9600);
  Wire.begin(); 

  // if (mySensor.begin() == false) {
  //   Serial.println("No SGP30 Detected. Check connections.");
  //   while (1);
  // }

  if(!pHSensor.begin()) {
    Serial.println("ERROR: couldn't detect the sensor");
    while(1){}
  }

  //   if(!drinkSensor.begin()) {
  //   Serial.println("ERROR: couldn't detect the sensor");
  //   while(1){}
  // }
   
  /*
   * init RGBW sensor with: 
   *  - 320ms integration time
   *  - auto mode
   *  - color sensor enable
   */
    
	pHSensor.setConfiguration(VEML6040_IT_80MS + VEML6040_AF_AUTO + VEML6040_SD_ENABLE);
  // drinkSensor.setConfiguration(VEML6040_2_IT_320MS + VEML6040_2_AF_AUTO + VEML6040_2_SD_ENABLE);
	
  delay(1500);
  Serial.println("Vishay VEML6040 RGBW color sensor auto mode example");
  Serial.println("CCT: Correlated color temperature in \260K");
  Serial.println("AL: Ambient light in lux");
  delay(1500);

  // mySensor.initAirQuality();
}

void loop() {
  byte pHRed = bitConvert(pHSensor.getRed());
  byte pHBlue = bitConvert(pHSensor.getBlue());
  byte pHGreen = bitConvert(pHSensor.getGreen());

  rgbToHsv(pHRed, pHGreen, pHBlue, Hue, Saturation, Value);

  Serial.print("RED: ");
  Serial.print(pHRed);  
  Serial.print(" GREEN: ");
  Serial.print(pHGreen);  
  Serial.print(" BLUE: ");
  Serial.print(pHBlue);  

  Serial.println(" ");
  Serial.print("The hue is: ");
  Serial.print(Hue);

      if (Hue >= 0 && Hue < 30)
  {
    Serial.print(" - Red");
  }
    if (Hue >= 30 && Hue < 60)
  {
    Serial.print(" - Orange");
  }
  if (Hue >= 60 && Hue < 120)
  {
    Serial.print(" - Yellow");
  }
  if (Hue >= 120 && Hue < 180)
  {
    Serial.print(" - Green");
  }
    if (Hue >= 180 && Hue < 240)
  {
    Serial.print(" - Cyan");
  }
  if (Hue >= 240 && Hue < 300)
  {
    Serial.print(" - Blue");
  }
    if (Hue >= 300 && Hue < 360)
  {
    Serial.print(" - Magenta");
  }

//   Serial.print(" WHITE: ");
//   Serial.print(RGBWSensor.getWhite()); 
//   Serial.print(" CCT: ");
//   Serial.print(RGBWSensor.getCCT());  
//   Serial.print(" AL: ");
//   Serial.println(RGBWSensor.getAmbientLight()); 
// delay (2000);
float pH = convertRGBtoPH(pHRed, pHGreen, pHBlue);

delay(2000);


if (pH !=-1)
  {
  Serial.println("");
  Serial.println("The estimated pH of this liquid is: ");
  Serial.print(pH);
  Serial.println("");

  delay(2000);
  }
  else 
  {
    Serial.println("");
    Serial.println("pH is invalid");
    Serial.println("");
    delay(2000);
  }

//   byte drinkRed = bitConvert(drinkSensor.getRed());
//   byte drinkBlue = bitConvert(drinkSensor.getBlue());
//   byte drinkGreen = bitConvert(drinkSensor.getGreen());

//   rgbToHsv(drinkRed, drinkGreen, drinkBlue, Hue, Saturation, Value);

//   Serial.print("drink RED: ");
//   Serial.print(drinkRed);  
//   Serial.print(" drink GREEN: ");
//   Serial.print(drinkGreen);  
//   Serial.print(" drink BLUE: ");
//   Serial.print(drinkBlue);  

//   Serial.println(" ");
//   Serial.print("The hue of the Beverage is: ");
//   Serial.print(Hue);
//   Serial.print(hueConvert(Hue));

//   delay(2000);
//   Serial.println(" ");
//   mySensor.measureAirQuality();
//   Serial.print("CO2: ");
//   Serial.print(mySensor.CO2);
//   Serial.println(" ppm");


}

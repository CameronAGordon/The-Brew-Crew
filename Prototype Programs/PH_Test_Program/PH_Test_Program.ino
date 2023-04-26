#include "Wire.h"
#include "veml6040.h"

VEML6040 RGBWSensor;

byte bitConvert(uint16_t valueRGB)
{
  float scaledRGB = (float)(valueRGB/(65535.0))*255.0;
  byte scaledRGB_byte = (byte)scaledRGB;
  return scaledRGB_byte; 
}

// pH to RGB Using Color Picker Tool Online
// pH 1 = rgb(186,58,55)
// pH 2 = rgb(225,75,77)
// pH 3 = rgb(249,146,67)
// pH 4 = rgb(236,143,37)
// pH 5 = rgb(244,173,19)
// pH 6 = rgb(244,249,22)
// pH 7 = rgb(254,212,100)
// pH 8 = rgb(200,169,102)
// pH 9 = rgb(111,98,63)
// pH 10 = rgb(98,88,76)
// pH 11 = rgb(73,70,127)
// pH 12 = rgb(67,46,65)
// pH 13 = rgb(48,31,50)
// pH 14 = rgb(62,31,37)

// Define RGB and pH data
// const byte red[] = {186, 225, 249, 236, 244, 244, 254, 200, 111, 98, 73, 67, 48, 62};
// const byte green[] = {58, 75, 146, 143, 173, 249, 212, 169, 98, 88, 70, 46, 31, 31};
// const byte blue[] = {55, 77, 67, 37, 19, 22, 100, 102, 63, 76, 127, 65, 50, 37};

byte rgbValues[14][3] = {
  {186,58, 55},
  {225,75,77},
  {249,146, 67},
  {236, 143, 37},
  {244, 173, 19},
  {244, 249, 22},
  {254, 212, 100},
  {200, 169, 102},
  {111, 98, 63},
  {98,88,76},
  {73, 70, 127},
  {67, 46, 65},
  {48, 31, 50},
  {62, 31, 37}
};

float Hue, Saturation, Value;

const float pHValues[14] = {1.0,2.0,3.0,4.0,5.0,6.0,7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0};

float convertRGBtoPH(int r, int g, int b) {
  for (int i = 0; i < 13; i++) {
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

void rgbToHsv(byte r, byte g, byte b, float &h, float &s, float &v) {
  float red = float(r) / 255.0;
  float green = float(g) / 255.0;
  float blue = float(b) / 255.0;

  float cmax = max(max(red, green), blue);
  float cmin = min(min(red, green), blue);
  float delta = cmax - cmin;

  if (delta == 0) {
    h = 0;
  } else if (cmax == red) {
    h = fmod((green - blue) / delta, 6.0);
  } else if (cmax == green) {
    h = ((blue - red) / delta) + 2;
  } else {
    h = ((red - green) / delta) + 4;
  }

  h = h * 60;
  if (h < 0) {
    h += 360;
  }

  s = (cmax == 0) ? 0 : delta / cmax;
  v = cmax;
}




void setup() {
  Serial.begin(9600);
  Wire.begin(); 



  if(!RGBWSensor.begin()) {
    Serial.println("ERROR: couldn't detect the sensor");
    while(1){}
  }
   
  /*
   * init RGBW sensor with: 
   *  - 320ms integration time
   *  - auto mode
   *  - color sensor enable
   */
    
	RGBWSensor.setConfiguration(VEML6040_IT_320MS + VEML6040_AF_AUTO + VEML6040_SD_ENABLE);
	
  delay(1500);
  Serial.println("Vishay VEML6040 RGBW color sensor auto mode example");
  Serial.println("CCT: Correlated color temperature in \260K");
  Serial.println("AL: Ambient light in lux");
  delay(1500);
}

void loop() {
  byte newRed = bitConvert(RGBWSensor.getRed());
  byte newBlue = bitConvert(RGBWSensor.getBlue());
  byte newGreen = bitConvert(RGBWSensor.getGreen());

  // Serial.print("RED: ");
  // Serial.print(newRed);  
  // Serial.print(" GREEN: ");
  // Serial.print(newGreen);  
  // Serial.print(" BLUE: ");
  // Serial.print(newBlue);  

 

  delay(500);

  rgbToHsv(newRed, newGreen, newBlue, Hue, Saturation, Value);
  Serial.print("The hue of the beverage is: ");
  Serial.print(Hue);
  Serial.println("");
//   Serial.print(" WHITE: ");
//   Serial.print(RGBWSensor.getWhite()); 
//   Serial.print(" CCT: ");
//   Serial.print(RGBWSensor.getCCT());  

// delay (2000);
// float pH = convertRGBtoPH(newRed, newGreen, newBlue);

// delay(2000);

// if (pH !=-1)
//   {
//     Serial.println("");
//   Serial.println("The estimated pH of this liquid is: ");
//   Serial.print(pH);
//   Serial.println("");

//   delay(2000);
//   }
//   else 
//   {
//     Serial.println("");
//     Serial.println("pH is invalid");
//     Serial.println("");
//     delay(2000);
//   }
}

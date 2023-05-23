# The-Brew-Crew

This code represents the DMMS Autums 2023 Coffee E-Nose Project for the University of Technology Sydney

NOTES:
- DO NOT USE THE GAS TEST PROGRAM. The gas sensor will take three minutes to warm-up and therefore is not practical for the prototype
- Devices are connected via I2C. The address for the colour sensor (VEML6040) is 0x10 and the CO2 Sensor (SGP30) is 0x58. You can also use the provided libraries under the sensor merge folder.
- The prototype programs folder contains code to run each sensor seperately if debugging is required

The sensor code was written in the Arduino IDE. The sensor collection code was written in VSCode using Python 3.11

Installed Libraries:
- VEML6040
- SparkFun_SGP30_Arduino_Library

You will also need to install the pyserial library using command prompt to collect data for each sensor

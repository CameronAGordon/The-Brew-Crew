# The-Brew-Crew

This code represents the DMMS Autums 2023 Coffee E-Nose Project for the University of Technology Sydney

NOTES:
- DO NOT USE THE GAS TEST PROGRAM. The gas sensor will take three minutes to warm-up and therefore is not practical for the prototype
- Devices are connected via I2C. The address for the colour sensor (VEML6040) is 0x10 and the CO2 Sensor (SGP30) is 0x58. You can also use the provided libraries under the sensor merge folder or those provided in this README document.
- The prototype programs folder contains code to run each sensor seperately if debugging is required
- These instructions are written for Windows. The code is untested in Mac or Linux.
- An Arduino Uno was used for this prototype

The sensor code was written in the Arduino IDE for easy library installation. You can download the latest Arduino IDE by following this link:
https://www.arduino.cc/en/software

The sensor data collection code was written in VSCode using Python 3.11.
You can download Python 3.11 on the Microsoft Store and you can download Visual Studio Code by following this link:
https://code.visualstudio.com/Download

Installed Libraries in Arduino IDE:
- VEML6040
- SparkFun_SGP30_Arduino_Library
You can use the library manager on the Arduino IDE to find these libraries

You will also need to install the pyserial library using command prompt to collect data for each sensor. Open Command Prompt as administrator and enter the command:
  pip install pyserial
If you have the 'serial' library installed, the data collection code will not run. If this is the case, run the command:
  pip uninstall serial
Make sure to restart the computer for these changes to take effect.

Make sure to change the COM Port value in both the Arduino and the Python code to reflect the COM port used in your system to power the Arduino. In the Arduino IDE, if you have an Arduino connected, you can determine the COM port being used using the drop-down menu and selecting: Tools -> Port. 


![image](https://github.com/CameronAGordon/The-Brew-Crew/assets/113693190/91634ec5-07c8-46db-8140-f68423b91de0). 


If you have multiple COM ports in use, select the one connected to the Arduino device. 





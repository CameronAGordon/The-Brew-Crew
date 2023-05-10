import csv
import serial
import time

filename = input("Enter the filename for the CSV output (without the extension): ")


# Open the serial port for communication with the Arduino
ser = serial.Serial('COM3', 9600)

# Open the CSV file for writing
with open(f"{filename}.csv", mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['RGB/Hue Values', 'CO2 Values'])

    # Continuously read data from the Arduino and write it to the CSV file
    while True:
        # Read a line of data from the Arduino
        line = ser.readline().decode('utf-8').strip()
        # Split the line into its component parts
        co2 = line.split()[1]
        red, green, blue = line.split()[3], line.split()[5], line.split()[7]
        hue = line.split()[9]
        color = line.split()[11]
        # Write the data to the CSV file
        writer.writerow([f"{red}, {green}, {blue}, {hue} - {color}", co2])
        # Wait for 0.1 seconds before reading the next line of data
        time.sleep(0.1)

import csv
import os
import serial
import time

filename = input("Enter the filename for the CSV output (without the extension): ")

# Get the absolute file path
file_path = os.path.abspath(f"{filename}.csv")
print("CSV file path:", file_path)

# Open the serial port for communication with the Arduino
ser = serial.Serial('COM8', 9600)

# Open the CSV file for writing
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time', 'Red', 'Green', 'Blue', 'Hue', 'Color'])

    # Continuously read data from the Arduino and write it to the CSV file
    while True:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
        except UnicodeDecodeError as e:
            print("Error decoding line:", e)
            continue

        if line.startswith("Invalid line format:") or line == "":
            # Ignore empty lines or lines with "Invalid line format"
            continue

        # Check if the line has the expected format for RGB values
        if line.startswith("RED:") and line.find("GREEN:") != -1 and line.find("BLUE:") != -1:
            # Extract the RGB values
            red_start = line.find("RED:") + len("RED:")
            red_end = line.find("GREEN:")
            green_start = line.find("GREEN:") + len("GREEN:")
            green_end = line.find("BLUE:")
            blue_start = line.find("BLUE:") + len("BLUE:")
            red = line[red_start:red_end].strip()
            green = line[green_start:green_end].strip()
            blue = line[blue_start:].strip()

            # Read the timestamp
            timestamp = line.split("->")[0].strip()

            # Write the RGB values to the CSV file
            writer.writerow([timestamp, red, green, blue, '', ''])

        # Check if the line has the expected format for hue and color
        elif line.startswith("The hue is: ") and line.find("-") != -1:
            # Extract the hue value
            hue_start = line.find("The hue is:") + len("The hue is:")
            hue_end = line.find("-", hue_start)
            hue = line[hue_start:hue_end].strip()

            # Extract the color value
            color_start = line.find("-", hue_end) + len("-")
            color = line[color_start:].strip()

            # Write the hue and color to the CSV file
            writer.writerow(['', '', '', '', hue, color])

        elif line == 'pH is invalid':
            # Write an invalid pH value to the CSV file
            writer.writerow(['', '', '', '', 'Invalid pH value', ''])

        else:
            print("Invalid line format:", line)

        # Wait for 0.1 seconds before reading the next line of data
        time.sleep(0.1)

    # Close the file
    file.close()

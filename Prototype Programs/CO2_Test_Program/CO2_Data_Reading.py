import serial
import csv
import time

# Ask the user to input the filename for the CSV output
filename = input("Enter the filename for the CSV output (without the extension): ")

# Open the serial port at the specified baud rate
ser = serial.Serial('COM4', 9600)

# Open the CSV file with the user-specified filename and create a writer object
with open(f"{filename}.csv", mode='w', newline='') as file:
    writer = csv.writer(file)

    # Write the header row to the CSV file
    writer.writerow(['time', 'CO2'])

    # Set the start time
    start_time = time.time()

    # Run the program for 30 seconds
    while time.time() - start_time < 30:
        # Read a line of data from the serial port
        line = ser.readline().decode('utf-8').rstrip()

        # Split the line into two parts: the time and the CO2 value
        parts = line.split(': ')
        if len(parts) == 2 and parts[0] == 'CO2':
            # Convert the CO2 value to an integer
            co2 = int(parts[1].split()[0])
            print(co2)

            # Get the current time
            t = time.time()

            # Write the time and CO2 value to the CSV file
            writer.writerow([t, co2])

            # Wait for 0.1 seconds before reading the next line
            time.sleep(0.1)
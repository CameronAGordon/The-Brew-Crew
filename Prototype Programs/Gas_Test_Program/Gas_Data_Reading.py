import serial
import csv
import time

# Open the serial port at the specified baud rate
ser = serial.Serial('COM4', 9600)

# Open the CSV file and create a writer object
with open('Gas.csv', mode='w', newline='') as file:
    time.sleep(185)
    writer = csv.writer(file)

    # Write the header row to the CSV file
    writer.writerow(['time', 'Gas'])

    # Continuously read data from the serial port and write it to the CSV file
    while True:
        # Read a line of data from the serial port
        line = ser.readline().decode('utf-8').rstrip()
       

        # Split the line into two parts: the time and the Gas value
        parts = line.split(': ')
        if len(parts) == 2 and parts[0] == 'Gas':
            # Convert the Gas value to an integer
            gas = int(parts[1].split()[0])
            print(gas)

            # Get the current time
            t = time.time()

            # Write the time and Gas value to the CSV file
            writer.writerow([t, gas])

            # Wait for 0.1 seconds before reading the next line
            #time.sleep(0.1)
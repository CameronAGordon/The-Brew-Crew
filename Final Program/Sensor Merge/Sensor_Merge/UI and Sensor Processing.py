import wx
import wx.grid
import serial
import time
import threading

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(500, 300))

        # create a panel to hold the UI elements
        panel = wx.Panel(self)

        # create a sizer to arrange the UI elements vertically
        vbox = wx.BoxSizer(wx.VERTICAL)

        # create the "Test Liquid" button and add it to the sizer
        btn_test_liquid = wx.Button(panel, label='Test Liquid')
        vbox.Add(btn_test_liquid, flag=wx.CENTER|wx.TOP|wx.BOTTOM, border=10)

        # create a table with the specified headings and add it to the sizer
        table = wx.grid.Grid(panel)
        table.CreateGrid(5, 1)
        table.SetColLabelValue(0, 'Value')
        table.SetRowLabelValue(0, 'CO2 Average')
        table.SetRowLabelValue(1, 'Red')
        table.SetRowLabelValue(2, 'Green')
        table.SetRowLabelValue(3, 'Blue')
        table.SetRowLabelValue(4, 'Hue')
        vbox.Add(table, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)

        # set the sizer for the panel
        panel.SetSizer(vbox)

        # center the window on the screen and show it
        self.Center()
        self.Show(True)

        # open the serial connection
        ser = serial.Serial('COM3', 9600)

        # start a new thread to read and store the data
        threading.Thread(target=self.read_serial_data, args=(ser, table)).start()

    def read_serial_data(self, ser, table):
        # initialize variables to store the data
        co2_data = []
        red_data = []
        green_data = []
        blue_data = []
        hue_data = []

        while True:
            # read the next line from the serial connection
            line = ser.readline().decode().strip()

            # parse the line for the sensor values
            if line.startswith('CO2:'):
                co2 = float(line.split()[1])
                co2_data.append(co2)
            elif line.startswith('RED:'):
                red = int(line.split()[1])
                green = int(line.split()[3])
                blue = int(line.split()[5])
                red_data.append(red)
                green_data.append(green)
                blue_data.append(blue)
            elif line.startswith('The hue of the beverage is:'):
                hue = int(line.split()[5])
                hue_data.append(hue)

            # check if enough data has been collected
            if len(co2_data) >= 300:
                # calculate the average of the last 10 readings for each variable
                co2_average = sum(co2_data[-10:]) / 10
                red_average = sum(red_data[-10:]) / 10
                green_average = sum(green_data[-10:]) / 10
                blue_average = sum(blue_data[-10:]) / 10
                hue_average = sum(hue_data[-10:]) / 10
                 # update the table with the new values
            table.SetCellValue(0, 0, str(co2_average))
            table.SetCellValue(1, 0, str(red_average))
            table.SetCellValue(2, 0, str(green_average))
            table.SetCellValue(3, 0, str(blue_average))
            table.SetCellValue(4, 0, str(hue_average))

            # clear the data lists
            co2_data = []
            red_data = []
            green_data = []
            blue_data = []
            hue_data = []

        # wait for a short time before reading the next line
        time.sleep(0.1)

app = wx.App()
MyFrame(None, title='Liquid Tester')
app.MainLoop()
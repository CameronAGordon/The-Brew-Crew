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
        self.btn_test_liquid = wx.Button(panel, label='Test Liquid')
        vbox.Add(self.btn_test_liquid, flag=wx.CENTER|wx.TOP|wx.BOTTOM, border=10)

        # bind the button to the on_test_liquid function
        self.btn_test_liquid.Bind(wx.EVT_BUTTON, self.on_test_liquid)

        # create a table with the specified headings and add it to the sizer
        self.table = wx.grid.Grid(panel)
        self.table.CreateGrid(5, 1)
        self.table.SetColLabelValue(0, 'Value')
        self.table.SetRowLabelValue(0, 'CO2 Average')
        self.table.SetRowLabelValue(1, 'Red')
        self.table.SetRowLabelValue(2, 'Green')
        self.table.SetRowLabelValue(3, 'Blue')
        self.table.SetRowLabelValue(4, 'Hue')
        vbox.Add(self.table, flag=wx.CENTRE|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)

        self.lbl_countdown = wx.StaticText(panel, label='Press The Button to Begin')
        vbox.Add(self.lbl_countdown, flag=wx.CENTER|wx.TOP|wx.BOTTOM, border=10)

        # add the "Result" textbox
        self.lbl_result = wx.StaticText(panel, label='Result')
        vbox.Add(self.lbl_result, flag=wx.CENTER | wx.TOP, border=10)

        # set the sizer for the panel
        panel.SetSizer(vbox)

        # center the window on the screen and show it
        self.Center()
        self.Show(True)

        # open the serial connection
        #self.ser = serial.Serial('COM4', 9600)


    def on_test_liquid(self, event):
        # initialize variables to store the data
        co2_data = []
        red_data = []
        green_data = []
        blue_data = []
        hue_data = []
        co2_average = 0
        red_average = 0
        green_average = 0
        blue_average = 0
        hue_average = 0
        duration = 30
        self.lbl_countdown.SetLabelText('Please wait 30 seconds')


        # define a function to run in a separate thread
        def read_serial():
            nonlocal co2_data, red_data, green_data, blue_data, hue_data
            start_time = time.time()
            while time.time() - start_time < duration:
                # read the next line from the serial connection
                line = self.ser.readline().decode('utf-8').rstrip()
                print(line)

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
                elif line.startswith('HUE:'):
                    hue = int(line.split()[1])  
                    hue_data.append(hue)


                # wait for a short time before reading the next line
                time.sleep(0.05)

        # start a new thread for the while loop
        thread = threading.Thread(target=read_serial)
        thread.start()
        self.lbl_countdown.SetLabelText('Data Collection Complete')

        # periodically update the GUI with the new data
        while thread.is_alive():
            if len(co2_data) >= 10:
                # calculate the average of the last 10 readings for each variable
                co2_average = sum(co2_data[-10:]) / 10
                red_average = sum(red_data[-10:]) / 10
                green_average = sum(green_data[-10:]) / 10
                blue_average = sum(blue_data[-10:]) / 10
                hue_average = sum(hue_data[-10:]) / 10

                # update the table with the new values
                self.table.SetCellValue(0, 0, str(co2_average))
                self.table.SetCellValue(1, 0, str(red_average))
                self.table.SetCellValue(2, 0, str(green_average))
                self.table.SetCellValue(3, 0, str(blue_average))
                self.table.SetCellValue(4, 0, str(hue_average))

                if 450 <= co2_average <= 500 or 60 <= hue_average <= 66:
                    result = 'Coffee'
                else:
                    result = 'Not Coffee'
                
                # update the result label
                self.lbl_result.SetLabelText(result)
                
                # clear the data lists
                co2_data = co2_data[-10:]
                red_data = red_data[-10:]
                green_data = green_data[-10:]
                blue_data = blue_data[-10:]
                hue_data = hue_data[-10:]

                

            # wait for a short time before checking again
            time.sleep(0.1)

app = wx.App()
MyFrame(None, title='Liquid Tester')
app.MainLoop()
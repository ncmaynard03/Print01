from serial import Serial
import XInput
import time

feedrates = [200, 500, 1000, 3000, 6000, 12000]
modes = {1 : "Relative", 2:"Absolute"}

MIN_PRINT_TEMP = 170
PREHEAT_HOTEND_TEMP = 200
PREHEAT_BED_TEMP = 75


class Printer:
    def __init__(self, port:str, baudrate:int, x:int = 230, y:int = 230, test:bool=False):
        ## Connection 
        self.test = test
        if not self.test:
            self.port = port
            self.baudrate = baudrate
            self.ser = Serial(port, baudrate)
            time.sleep(5) # Wait for printer to reset
        self.output_line("M117 Hello World!") # dDisplay to LCD
        self.preheat()
        
        ## Printer specs
        self.x = x
        self.y = y
        self.hotend_temp = 0
        self.bed_temp = 0

        ## Printer variables
        self.set_relative()
        self.fr_index = 4
        self.increase_feedrate()
        print(feedrates[self.fr_index])
        
    def increase_feedrate(self):
        self.fr_index = min(len(feedrates) - 1, self.fr_index + 1)
        self.output_line("G0 F" + str(feedrates[self.fr_index]))
        
    def decrease_feedrate(self):
        self.fr_index = max(len(feedrates), 0)
        self.output_line("G0 F" + str(feedrates[self.fr_index]))

    def home(self, x:bool = True, y:bool = True, z:bool = True):
        line = "G28"
        if not (x and y and z):
            if x:
                line += " X"
            if y: 
                line += " Y"
            if z:
                line += " Z"
        self.output_line(line)

    def home_x(self):
        self.home(y=False, z=False)

    def home_y(self):
        self.home(x=False, z=False)

    def home_xy(self):
        self.home(z = False)

    def home_z(self):
        self.home(x=False, y=False)

    def set_relative(self):
        self.output_line("G91")
        self.relative = True

    def set_absolute(self):
        self.output_line("G90")
        self.relative = False
        
    def move(self, e:int=0, x:int = 0, y:int = 0, z:int = 0):
        if e == x == y == z == 0:
            return
        line = "G0"
        if e != 0 and self.hotend_temp > MIN_PRINT_TEMP:
            line += " E" + str(e)
        if x != 0:
            line += " X" + str(x)
        if y != 0:
            line += " Y" + str(y) 
        if z!= 0:
            line += " Z" + str(z)

        self.output_line(line)

    def preheat(self, hotend=True, bed=True):
        if hotend:
            self.set_hotend_temp(PREHEAT_HOTEND_TEMP)
        if bed:
            self.set_bed_temp(PREHEAT_BED_TEMP)


    def set_hotend_temp(self, temp, wait:bool = False):
        if wait: 
            cmd = "M109 S"
        else:
            cmd = "M104 S"
        self.output_line(cmd + str(temp))
        self.hotend_temp = temp

    def set_bed_temp(self, temp:int, wait:bool = False):
        if wait:
            cmd = "M190 S"
        else:
            cmd = "M140 S"
        self.output_line(cmd + str(temp))
        self.bed_temp = temp

    def cooldown(self):
        self.set_hotend_temp(0)
        self.set_bed_temp(0)
        
    

    def output_line(self, line:str):
        print(line)
        line += "\r\n"
        if not self.test:
            self.ser.write(line.encode())

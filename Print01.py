from printer import Printer
from controller import Controller
import serial.tools.list_ports
import tkinter as tk
import time

window = tk.Tk()

ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
    print(port, desc, hwid)

ptr = Printer("com4", 112000, test=True)
control_mode_enabled = False
ptr.home()


if control_mode_enabled:

    ctr = Controller(0)
    while True:
        ctr.update_state()
        btn_vals = ctr.get_btn_values()
        if btn_vals['LEFT_THUMB'] == 1:
            ptr.home_xy()
        if btn_vals['RIGHT_THUMB'] == 1:
            ptr.home()
        if btn_vals['X'] == 1:
            ptr.preheat()
        if btn_vals['B'] == 1:
            ptr.cooldown()
        ptr.move(ctr.get_trigger_axis() * .1, ctr.get_xl() * 5, ctr.get_yl() * 5, ctr.get_yr() * 2/3)   
        time.sleep(.02) 
        ctr.get_btn_values()

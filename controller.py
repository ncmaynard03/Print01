import XInput

class Controller:
    def __init__(self, index):
        self.index = index
        self.deadzone = 0.15
        self.update_state()

    def update_state(self):
        self.state = self.get_state()
        self.btn_values = XInput.get_button_values(self.state)
        #print(XInput.get_button_values(self.state))

    

    def get_state(self):
        return XInput.get_state(self.index)
    
    def get_xl(self):
        value = XInput.get_thumb_values(self.state)[0][0]
        return value if abs(value) > self.deadzone else 0

    def get_yl(self):
        value = XInput.get_thumb_values(self.state)[0][1]
        return value if abs(value) > self.deadzone else 0
    
    def get_xr(self):
        value = XInput.get_thumb_values(self.state)[1][0]
        return value if abs(value) > self.deadzone else 0
    
    def get_yr(self):
        value = XInput.get_thumb_values(self.state)[1][1]
        return value if abs(value) > self.deadzone else 0
    
    def get_ltrigger(self):
        value = XInput.get_trigger_values(self.state)[0]
        return value if abs(value) > self.deadzone else 0
    
    def get_trigger_axis(self):
        value = self.get_rtrigger() - self.get_ltrigger()
        return value if abs(value) > self.deadzone else 0
    
    def get_rtrigger(self):
        value = XInput.get_trigger_values(self.state)[1]
        return value if abs(value) > self.deadzone else 0
    
    def get_lthumb_btn(self):
        return XInput.get(self.state)[0]
    
    def get_btn_values(self):
        value = XInput.get_button_values(self.state)
        return value
    
    
"""
Simple demo PID

Jon V
30/05/2014
"""

import time

class PID:
    def __init__(self):
        self.last_time = time.time()
        self.error_sum = 0
        
        self.kp = 0.9
        self.ki = 0.1


    def reset(self):
        self.error_sum = 0
        
        
    def tune(self, kp, ki):
        self.kp = kp
        self.ki = ki
        

    def compute(self, current, setpoint):
        now = time.time()
        timedelta = now - self.last_time
        if timedelta == 0:
            now = time.time()
            timedelta = now - self.last_time
            
        error = setpoint - current
        self.error_sum +=  (error * timedelta)

        self.last_time = now

        return (self.kp * error) + (self.ki * self.error_sum)


if __name__ == '__main__':
    
    pid = PID()
    current = -65.0
    target = 0.0

    while True:
        comp = pid.compute(current, target)
        print comp, current
        current = comp
        time.sleep(0.1)

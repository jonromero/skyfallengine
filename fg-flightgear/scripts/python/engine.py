"""
First Demo Engine

Jon V (darksun4@gmail.com)
30/05/2014
"""

from FlightGear import FlightGear
import time
from datetime import datetime
from PID import PID

fg = FlightGear('localhost', 5500)

def main():

    # Wait five seconds for simulator to settle down
    while 1:
        if fg['/sim/time/elapsed-sec'] > 5:
            break
        time.sleep(1.0)
        print fg['/sim/time/elapsed-sec']


    # parking brake on
    fg['/controls/parking-brake'] = 1

    #heading = fg['/orientation/heading-deg']

    # Switch to external view for for 'walk around'.
    fg.view_next()

    fg['/sim/current-view/goal-heading-offset-deg'] = 180.0
    #fg.wait_for_prop_eq('/sim/current-view/heading-offset-deg', 180.0)

    fg['/sim/current-view/goal-heading-offset-deg'] = 90.0
    #fg.wait_for_prop_eq('/sim/current-view/heading-offset-deg', 90.0)

    fg['/sim/current-view/goal-heading-offset-deg'] = 0.0
    #fg.wait_for_prop_eq('/sim/current-view/heading-offset-deg', 0.0)

    time.sleep(2.0)

    # Switch back to cockpit view
    fg.view_prev()

    time.sleep(2.0)

    # Flaps to take off position
    #fg['/controls/flaps'] = 0.0
    #fg.wait_for_prop_eq('/surface-positions/flap-pos-norm', 0.34)

    stabilize_height(30000)
    #fg['/controls/flight/aileron'] = 0.00   #-1 to 1
    #fg['/controls/flight/elevator'] = 0.00
    
    fg.quit()


def map_to_range(x, in_min, in_max, out_min, out_max):
    val = (((x - in_min) * (out_max - out_min))/(float)(in_max - in_min))+out_min
    if val > out_max:
        val = out_max
    elif val < out_min:
        val = out_min

    return val 
    

def stabilize_height(height):
    done = True
    pid_pitch = PID()
    pid_roll = PID()
    i = 0

    fd = open("flight_data.csv", "w")
    fd.write("timestamp, pitch, roll, elevator, aileron, height, airspeed\n")
    
    while(done):
        i += 1

        # more about properties here
        # http://wiki.flightgear.org/Property_Tree/Reference
        current_height = fg['/position/altitude-ft/']
        current_airspeed = fg['/velocities/airspeed-kt']
        current_roll = fg['/orientation/roll-deg']
        current_pitch = fg['/orientation/pitch-deg']
        
        print "Pitch:", current_pitch
        print "Roll:", current_roll
        print "Airspeed", current_airspeed
        
        output_pitch = pid_pitch.compute(current_pitch, 1)
        output_roll = pid_roll.compute(current_roll, 1)

        print "Out Pitch:", output_pitch
        print "Out Roll:", output_roll

        mapped_pitch = map_to_range(output_pitch, 90, -90, -1, 1)
        mapped_roll = map_to_range(output_roll, -180, 180, -1, 1)

        if abs(output_roll)> 180 or abs(output_pitch)> 180:
            pid_pitch.reset() 
            pid_roll.reset()
            print "RESETTING algorithm"            
            i = 0

        if i > 100:
            print "RESET"
            i = 0
            pid_pitch.reset() 
            pid_roll.reset()
            time.sleep(0.1)

        fg['/controls/flight/aileron'] = mapped_roll
        fg['/controls/flight/elevator'] = mapped_pitch

        print "Elevator:", mapped_pitch
        print "Aileron:", mapped_roll
        print "----------"

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fd.write("%s, %f, %f, %f, %f, %f, %f\n" % (current_time, current_pitch, current_roll, mapped_pitch, mapped_roll, current_height, current_airspeed))
        fd.flush()
        #time.sleep(0.01)

    close(fd)

main()


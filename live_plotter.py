import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np

import time
import random

import json
from serial import *

from threading import Thread

# NOTE: Change this to wherever your usb connection is
ser = Serial('/dev/cu.usbmodem1421', 9600)

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = [0]
a_x = [0]
a_y = [0]
a_z = [0]
ys = [1]

accel = [[0], [0], [0]]


#f = open('Salmon_presure_test.txt')

def nextTemp():
    try:
        data = json.loads(last_received)
        temp = data['bmi1']['a']
        tick = data['tick']
        print(tick)
        return temp, tick
    except:
        pass

    return -1, -1

last_received = ''
def receiving(ser):
    global last_received
    buff = ''

    while True:
        # last_received = ser.readline()

        buff += ''.join([chr(c) for c in ser.read(200)])
        if '\n' in buff:
            last_received, buff = buff.split('\n')[-2:]
        #time.sleep(0.1)


# This function is called periodically from FuncAnimation
def animate(i, xs, accel):

    # Read temperature (Celsius) from TMP102
    #temp_c = ys[-1] + random.randint(-4, 4)
    a, tick = nextTemp()
    if tick == -1:
        return
    # Add x and y to lists
    #xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    xs.append(xs[-1]+1)
    #ys.append(accel[0])
     

    accel[0].append(a[0])
    accel[1].append(a[1])
    accel[2].append(a[2])

    #a_x.append(accel[0])
    #a_y.append(accel[1])
    #a_z.append(accel[2])

    # Limit x and y lists to 20 items
    xs = xs[-100:]
    accel[0] = accel[0][-100:]
    accel[1] = accel[1][-100:]
    accel[2] = accel[2][-100:]
    #a_x = a_x[-100:]
    #a_y = a_y[-100:]
    #a_z = a_z[-100:]
    #ys = ys[-100:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, accel[0], 'r-', label='accel.x')    
    ax.plot(xs, accel[1], 'g-', label='accel.y')
    ax.plot(xs, accel[2], 'b-', label='accel.z')

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.1, left=0.1)
    plt.title('Acceleration over Time')
    plt.legend()
    plt.grid()
    plt.ylabel('m/s^2')


Thread(target=receiving, args=(ser,)).start()

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, accel), interval=1)
plt.show()


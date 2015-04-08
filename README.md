Project 04: Telekinesis Car
===========================
*Devin Delfino*

Description
-----------
Uses the MUSE headband, Arduino UNO, and a remote control toy car to create a 'Telekinesis Car'! One option is to control the toy car using keyboard controls. A second option is to control the car using blinks, winks, and jaw clenches. A third option is to relax your mind, emmitting alpha brain waves that trigger the car to move forward.

Setup
-----
1. Connect the soldered remote control circuitboard to the Arduino UNO. Connect the 'forward' wire to pin 2, the 'backward' wire to pin 4, the 'left' wire to pin 8, the 'right' wire to pin 12, the '+' wire to pin 3.3v, and the '-' wire to pin GND.
2. Load *arduino/muse_control.ino* onto the Arduino (keep it connected to computer).
3. Alter the **arduinoPort** variable (line 26) in *signal_relax.py* to match the port on which the Arduino is connected.
4. Connect the MUSE headband to the computer via bluetooth.
5. In one terminal, run the following command:

muse-io --dsp --osc osc.udp://localhost:5000

6. In a second terminal, run the following command (*threshold* is a float between 0 and 1 defining the level of relaxtion needed to move the car):

python signal_relax.py -t *threshold*

7. Think!

Note: The same instructions apply for *signal_blink.py*.

Usage
-----
**Keyboard Controls**
* *Pre* - Load *arduino/keyboard_control.ino* onto the arduino and open the serial monitor.
* *d* - moves the car forward
* *s* - moves the car backward
* *a* - turns the car left
* *f* - turns the car right
* *x* - stops the car

**Blink Controls**
* *Pre* - Load *arduino/muse_control.ino* onto the arduino, run the *muse-io* command (see setup), and run *signal_blink.py*
* *BLINK* - moves car forward (if car is stopped or moving backwards)
* *BLINK* - moves car backwards (if car is moving forward)
* *LEFT EYE WINK* - turns the car left
* *RIGHT EYE WINK* - turns the car right
* *JAW CLENCH* - stops the car

**Meditation Controls**
* *Pre* - Load *arduino/muse_control.ino* onto the arduino, run the *muse-io* command (see setup), and run *signal_relax.py*
* Simply try to quiet and relax your mind. The alpha brain waves that are associating with relaxation will trigger the car to move forward.


Contents
--------
* *signal_relax.py* - python script that notifies the arduino using blinks, jaw clenches, and winks to control the car.
* *signal_blink.py* - python script that notifies the arduino using relaxing brainwaves.
* *arduino/muse_control.ino* - arduino script that accepts commands from the MUSE (from python scripts)
* *arduino/keyboard_control.ino* - arduino script that accepts keyboard input from serial port


Requirements
------------
* Arduino UNO
* [MUSE](http://www.choosemuse.com/) headband.
* Toy Car with remote control (New Bright 1:24 Scale Radio Control Sports Car is used in the tutorial)
* liblo and pyliblo

References
-----------

1. This project is heavily based on this [IBM developerWorks Tutorial](http://www.ibm.com/developerworks/library/ba-muse-toycar-app/index.html) by Thiago Domingues, Lucas Lima, and Raul Chong.

#!/usr/bin/env python

import liblo, sys, serial, time, requests, json, math, datetime, os, Queue
from websocket import create_connection
from threading import Thread, Lock

# List of all the inputs coming from Muse
arduinoValues = Queue.Queue()
arduinoHorseShoe = Queue.Queue()
arduinoTouchingForehead = Queue.Queue()
localValues = Queue.Queue()
localHorseShoe = Queue.Queue()
localTouchingForehead = Queue.Queue()
localBatt = Queue.Queue()

# Other global variables
serialTransferRate = 115200
arduinoPort = '/dev/tty.usbmodem411'
localhost = 5000;
stopAllThreads = False
threshold = 0.35
moving_forward = False

# Looks for an arduino on the serial ports
def connectToArduino():
    print "Connecting to arduino on " + arduinoPort + " at " + str(serialTransferRate) + " baud"

    arduino = serial.Serial(arduinoPort, serialTransferRate)

    arduino.timeout = None
    time.sleep(2)
    arduino.write("S\n")
    print "Connected!"
    return arduino
      
# Controls the arduino
def sendToArduino(arduino):

  while(True):
    if(stopAllThreads):
      return True;
   
            

# # Reads the data from Muse and stores it on the inputsList
def processAlpha(path, args):
  for i in xrange(len(args)):
      if math.isnan(args[i]):
          args[i] = 0
  args.append(str(datetime.datetime.now()))
  arduinoValues.put(args)
  localValues.put(args)

def wink_event(path, args):
  if(not stopAllThreads):
    if(args[1] > 1000.0):
      # arduinoValues.put("L")
      arduino.write("L\n")
      print "Message to Arduino: <LEFT> \t" + "left wink"
    elif(args[2] > 1000.0):
      # arduinoValues.put("R")
      arduino.write("R\n")
      print "Message to Arduino: <RIGHT> \t" + "right wink"

def blink_event(path, args):
  if(not stopAllThreads):
    if(args[0] == 1):
      global moving_forward
      # print 'blinked!'
      if(not moving_forward): #moving forward
        moving_forward = True
        # arduinoValues.put("F")
        arduino.write("F\n")
        print "Message to Arduino: <FORWARD> \t" + "blinked"
      else: # moving backward
        moving_forward = False
        # arduinoValues.put("B")
        arduino.write("B\n")
        print "Message to Arduino: <BACKWARD> \t" + "blinked"

def jaw_clench_event(path, args):
  if(not stopAllThreads):
    if(args[0] == 1):
      # print 'clenched jaw!'
      # arduinoValues.put("S")
      arduino.write("S\n")
      print "Message to Arduino: <STOP> \t" + " clenched jaw"

# # Reads the data from Muse and stores it on the inputsList
def processBatt(path, args):
  # print args
  for i in xrange(len(args)):
      if math.isnan(args[i]):
          args[i] = 0
  args.append(str(datetime.datetime.now()))
  localBatt.put(args)


# # Reads the data from Muse and stores it on the inputsList
def processHorseShoe(path, args):
    localHorseShoe.put(args)


# # Reads the data from Muse and stores it on the inputsList
def processTouchingForehead(path, args):
    localTouchingForehead.put(args)

# Checking flag

if(len(sys.argv) == 1):
  print "Default threshold is " + str(threshold)
elif(len(sys.argv) == 3):
  print "Setting threshold to " + sys.argv[2]
  threshold = float(sys.argv[2])
else:
  print "Invalid number of parameters!"
  exit(1)

# create server, listening on port 5000
try:
    server = liblo.ServerThread(localhost, liblo.UDP)
except liblo.ServerError, err:
    print str(err)
    sys.exit()




# Registering the functions to be loaded for each OSC channel
server.add_method("/muse/eeg", 'ffff', wink_event)
server.add_method("/muse/elements/jaw_clench", 'i', jaw_clench_event)
server.add_method("/muse/elements/blink", 'i', blink_event)
server.add_method("/muse/dsp/elements/alpha", 'ffff', processAlpha)
server.add_method("/muse/batt", 'iiii', processBatt)
server.add_method("/muse/dsp/elements/horseshoe", 'ffff', processHorseShoe)
server.add_method("/muse/dsp/elements/touching_forehead", 'i', processTouchingForehead)
server.add_method("/muse/dsp/elements", 'i', processTouchingForehead)

# Starting server and threads
arduino = connectToArduino()

# SET THE URL OF THE NODEJS APP
#Note: remember that is a "ws" (web socket) connection
# connection = create_connection(webAppURL)


threadArduino = Thread(target=sendToArduino, args=[arduino])
# threadLocalServer = Thread(target=sendToLocal, args=[connection])

# Starts the threads and the OSC server
threadArduino.start()
# threadLocalServer.start()
server.start()


sys.stdin.readline()

print "Closing everything..."

stopAllThreads = True
print "Waiting for threads to close..."
arduino.write("S\n")
threadArduino.join(1.0)
print "Arduino thread closed!"
# threadLocalServer.join()

print "Local server thread closed!"

print "Waiting for OSC server to close..."
server.stop()
print "OSC server closed!"
# sys.exit()
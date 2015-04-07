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
arduinoPort = '/dev/tty.usbmodem1411'
# webAppURL = 'ws://movetoycar.mybluemix.net'
stopAllThreads = False
threshold = 0.35


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
  while (not stopAllThreads):
    # print "reading"
    c = arduino.read()
    # print c
    reading = arduinoValues.get(block=True)
    # print "read"
    arduinoValues.queue.clear()
    if (reading[0]+reading[1]+reading[2]+reading[3])/4 > threshold:
      arduino.write("F\n")
      print "Message to Arduino: <FORWARD> \t" + str((reading[0]+reading[1]+reading[2]+reading[3])/4)
    else:
      arduino.write("S\n")
      print "Message to Arduino: <STOP> \t" + str((reading[0]+reading[1]+reading[2]+reading[3])/4)
            
def sendToLocal(connection):
  while (not stopAllThreads):
    value = localValues.get(block=True)
    localValues.queue.clear()
    
    statusIndicator = localHorseShoe.get()
    localHorseShoe.queue.clear()
    
    touchingForehead = localTouchingForehead.get()
    localTouchingForehead.queue.clear()

    try:
      batt = localBatt.get(block=False)
      localBatt.queue.clear()
    except Queue.Empty:
      batt = [0,0,0,0]
    
    connection.send(json.dumps({
      'C0':value[0],
      'C1':value[1],
      'C2':value[2],
      'C3':value[3],
      'B0':batt[0],
      'B1':batt[1],
      'B2':batt[2],
      'B3':batt[3],
      'S0':statusIndicator[0],
      'S1':statusIndicator[1],
      'S2':statusIndicator[2],
      'S3':statusIndicator[3],
      'S3':statusIndicator[3],
      'F':touchingForehead[0],
      'timestamp':value[4]
      }))
    


# Reads the data from Muse and stores it on the inputsList
def processAlpha(path, args):
  # print args
  for i in xrange(len(args)):
      if math.isnan(args[i]):
          args[i] = 0
  args.append(str(datetime.datetime.now()))
  arduinoValues.put(args)
  localValues.put(args)

# Reads the data from Muse and stores it on the inputsList
def processBatt(path, args):
  # print args
  for i in xrange(len(args)):
      if math.isnan(args[i]):
          args[i] = 0
  args.append(str(datetime.datetime.now()))
  localBatt.put(args)


# Reads the data from Muse and stores it on the inputsList
def processHorseShoe(path, args):
    localHorseShoe.put(args)


# Reads the data from Muse and stores it on the inputsList
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
    server = liblo.ServerThread(5000, liblo.UDP)
except liblo.ServerError, err:
    print str(err)
    sys.exit()




# Registering the functions to be loaded for each OSC channel
server.add_method("/muse/dsp/elements/alpha", 'ffff', processAlpha)
server.add_method("/muse/batt", 'iiii', processBatt)
server.add_method("/muse/dsp/elements/horseshoe", 'ffff', processHorseShoe)
server.add_method("/muse/dsp/elements/touching_forehead", 'i', processTouchingForehead)
server.add_method("/muse/dsp/elements", 'i', processTouchingForehead)

# Starting server and threads
arduino = connectToArduino()

# SET THE URL OF THE NODEJS APP
#Note: remember that is a "ws" (web socket) connection
connection = create_connection(webAppURL)



threadArduino = Thread(target=sendToArduino, args=[arduino])
threadLocalServer = Thread(target=sendToLocal, args=[connection])

# Starts the threads and the OSC server
threadArduino.start()
threadLocalServer.start()
server.start()


sys.stdin.readline()

print "Closing everything..."

stopAllThreads = True
print "Waiting for threads to close..."
threadArduino.join()
print "Arduino thread closed!"
threadLocalServer.join()

# Stopping the car
arduino.write("S\n")

print "Local server thread closed!"

print "Waiting for OSC server to close..."
server.free()
print "OSC server closed!"
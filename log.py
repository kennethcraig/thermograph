#!/bin/python

import sys, sqlite3, argparse, os

w1BusPath = "/sys/bus/w1/devices/"
insideDeviceId = "28-0000044ae1aa"
outsideDeviceId = "28-0000044ae1aa"

def main():
	#parser = argparse.ArgumentParser(description='Logs a single inside & outside temperature into the DB.')
	#parser.add_argument('insideraw', type=int, help='The raw inside temp (integer)')
	#parser.add_argument('outsideraw', type=int, help='The raw outside temp (integer)')
	#args = parser.parse_args()
	
	# check if the bus is active
	if os.path.exists( w1BusPath ) == False:
		print "Cannot find 1-wire bus. Please ensure the w1_gpio module is loaded"
		sys.exit(1)
	
	
	logTemp( readTempFromDevice( insideDeviceId ), readTempFromDevice( outsideDeviceId ) )
	
def readTempFromDevice(deviceId):
	crc = "NO"
	while(crc == "NO"):
		sensorFile = open(w1BusPath + deviceId + "/w1_slave")
		sensorData = sensorFile.read()
		sensorFile.close()
		firstline = sensorData.split("\n")[0]
		crc = firstline.split(" ")[11]
		
	secondline = sensorData.split("\n")[1]
	
	# Split the line into words, referring to the spaces, and select the 10th word (counting from 0).
	temperatureData = secondline.split(" ")[9]
	
	# The first two characters are "t=", so get rid of those and convert the temperature from a string to a number.
	temperature = float(temperatureData[2:])
	
	# Put the decimal point in the right place and display it.
	temperature = temperature / 1000
		
      	return temperature
      		
def logTemp(insideTemp, outsideTemp):
	try:
		con = sqlite3.connect("temp.db")
		cur = con.cursor()
		cur.execute("""INSERT INTO temperatures 
						(
							tempInside, tempOutside, timestamp
						)
						VALUES
						(
							?, ?, datetime('now')
						)
					""",
					( insideTemp, outsideTemp )
		)
		con.commit()
		print "Temperature logged."

	except sqlite3.Error, e:
		print "Error: %s: " % e.args[0]
	finally:
		if con:
			con.close()

if __name__ == "__main__":
    main()

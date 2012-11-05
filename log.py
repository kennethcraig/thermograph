#!/bin/python

import sys, sqlite3, argparse

def main():
	parser = argparse.ArgumentParser(description='Logs a single inside & outside temperature into the DB.')
	parser.add_argument('insideraw', type=int, help='The raw inside temp (integer)')
	parser.add_argument('outsideraw', type=int, help='The raw outside temp (integer)')
	args = parser.parse_args()
	logTemp( args.insideraw, args.outsideraw )
	
def logTemp(rawInsideTemp, rawOutsideTemp):
	try:
		con = sqlite3.connect("temp.db")
		cur = con.cursor()
		cur.execute("""INSERT INTO temperatures 
						(
							rawTempInside, rawTempOutside, tempInside, tempOutside, timestamp
						)
						VALUES
						(
							?, ?, ?, ?, datetime('now')
						)
					""",
					( rawInsideTemp, rawOutsideTemp, rawInsideTemp / 100.0, rawOutsideTemp / 100.0 )
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

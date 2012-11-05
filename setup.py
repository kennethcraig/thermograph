#!/bin/python

import sqlite3
import sys

con = None

tableSQL = """

CREATE TABLE temperatures
(
	id INTEGER PRIMARY KEY,
	tempInside REAL,
	tempOutside REAL,
	timestamp INTEGER
);

"""

print "Initialising tables:"
try:
	con = sqlite3.connect("temp.db")
	cur = con.cursor()
	cur.execute(tableSQL);
	print "Complete."

except sqlite3.Error, e:
	print "Error: %s when inserting tables" % e.args[0]
	sys.exit(1)
finally:
	if con:
		con.close()

#!/usr/bin/python

import gpxpy
import sys	
from dateutil import tz

LOCAL_TZ = 'Asia/Singapore'

def get_loca_time(dt):
	local_tz = tz.gettz(LOCAL_TZ)
	dt = dt.replace(tzinfo=tz.gettz('UTC'))
	return dt.astimezone(to_zone)

def parse_gpx_file(filename):
    gpx_file = open(filename, 'r')
    gpx = gpxpy.parse(gpx_file)	
    for track in gpx.tracks:
	    for segment in track.segments:
	        for point in segment.points:
	        	print(
	        		get_loca_time(point.time), 
	        		point.latitude, 
	        		point.longitude, 
	        		point.elevation
	        	)

def main(args):
    gpx_file = args[0]

    parse_gpx_file(gpx_file)

if __name__ == "__main__":
    main(sys.argv[1:])
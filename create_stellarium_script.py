#!/usr/bin/python

import random
import gpxpy
import pyproj
import sys	
from dateutil import tz

LOCAL_TZ = 'Asia/Singapore'

# python3 create_stellarium_script.py data/Morning_Run.gpx 

def get_local_time(dt):
	local_tz = tz.gettz(LOCAL_TZ)
	dt = dt.replace(tzinfo=tz.gettz('UTC'))
	return dt.astimezone(tz.gettz(LOCAL_TZ))

def parse_gpx_file(filename):
	points = []

	gpx_file = open(filename, 'r')
	gpx = gpxpy.parse(gpx_file)

	for track in gpx.tracks:
		for segment in track.segments:
			for point in segment.points:
				points.append((
					get_local_time(point.time), 
					point.longitude, 
					point.latitude, 
					point.elevation					
				))

	return points

def get_bearing(points):
	for idx, point in enumerate(points, start=1):
		# We need to offset since points are very close
		previous_point = points[
			idx - random.randint(5, 10)
		]

		G = pyproj.Geod(ellps='WGS84')

		fwd_azimuth = G.inv(
			float(previous_point[1]),
			float(previous_point[2]),
			float(point[1]),
			float(point[2])
		)[0]

		print(
			point[0],
			point[1],
			point[2],
			point[3],
			fwd_azimuth
		)

def main(args):
	gpx_file = args[0]

	points = parse_gpx_file(gpx_file)
	get_bearing(points)

if __name__ == "__main__":
    main(sys.argv[1:])
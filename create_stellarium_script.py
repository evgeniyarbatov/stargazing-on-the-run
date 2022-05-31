#!/usr/bin/python

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
					point.latitude, 
					point.longitude, 
					point.elevation					
				))

	return points

def get_bearing(points):
	for idx, point in enumerate(points, start=1):
		geodesic = pyproj.Geod(ellps='WGS84')

		previous_point = points[idx-1]

		fwd_azimuth, back_azimuth, distance = geodesic.inv(
			previous_point[2],
			previous_point[1],
			point[2], 
			point[1]
		)

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
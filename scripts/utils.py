import gpxpy
import pytz

import xml.etree.ElementTree as ET

class Point:
	def __init__(
		self, 
		date,
		timestamp,
		lat,
		lon,
		az,
	):
		self.date = date
		self.timestamp = timestamp

		self.lat = float(lat)
		self.lon = float(lon)

		self.az = az

	def __str__(self):
		return f"date: '{self.date}', timestamp: {self.timestamp}, lat: {self.lat}, lon: {self.lon}, az: {self.az}"

class GPXData:
	def __init__(
		self,
		filename,
		timezone,
	):
		self.points = []

		with open(filename, 'r') as gpx_file:
			gpx = gpxpy.parse(gpx_file)
   
		gpx.simplify()

		compass_data = self.get_compass(filename)

		for track in gpx.tracks:
			for segment in track.segments:
				for point in segment.points:
					dt = point.time.replace(
						tzinfo=pytz.UTC
					)
					local_time = dt.astimezone(
						pytz.timezone(timezone)
					)

					az = self.get_compass_reading(
						compass_data, 
						point.time,
					)

					self.points.append(
						Point(
							local_time.strftime('%Y-%m-%dT%H:%M:%S'), 
							local_time.strftime('%s'), 
							point.latitude, 
							point.longitude,
							az,
						)
					)

	def get_compass(self, filename):
		compass_data = {}
     
		root = ET.parse(filename).getroot()
		for trk in root.findall('.//{http://www.topografix.com/GPX/1/1}trk'):
			for trkseg in trk.findall('{http://www.topografix.com/GPX/1/1}trkseg'):
				for trkpt in trkseg.findall('{http://www.topografix.com/GPX/1/1}trkpt'):
					time = trkpt.find('{http://www.topografix.com/GPX/1/1}time')
					time = time.text if time is not None else None
					
					extensions = trkpt.find('{http://www.topografix.com/GPX/1/1}extensions')
					if extensions is not None:
						compass = extensions.find('{http://www.topografix.com/GPX/1/1}compass')
						compass = float(compass.text) if compass is not None else None

						compass_data[time] = float(compass)
						
		return compass_data

	def get_compass_reading(self, compass_data, time):
		time = time.strftime('%Y-%m-%dT%H:%M:%SZ')
		return compass_data[time]

	def get_points(self):
		return self.points	
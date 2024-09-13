import gpxpy
import pytz

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

		for track in gpx.tracks:
			for segment in track.segments:
				for point in segment.points:
					dt = point.time.replace(
						tzinfo=pytz.UTC
					)
					local_time = dt.astimezone(
						pytz.timezone(timezone)
					)

					self.points.append(
						Point(
							local_time.strftime('%Y-%m-%dT%H:%M:%S'), 
							local_time.strftime('%s'), 
							point.latitude, 
							point.longitude,
							"0",
						)
					)

	def get_points(self):
		return self.points	
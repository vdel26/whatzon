import random, csv, math
import MySQLdb


class DB(object):
	def __init__(self):
		"""connect to local mysql"""
		self.db = MySQLdb.connect(host="localhost", port=8889, 
			user="root", passwd="root", db="places")
		self.cursor = self.db.cursor()	
	

	def select_all(self):
		"""select all from places.locations"""
		self.cursor.execute('SELECT * from locations')
		return self.cursor.fetchall()


	def search_nearby1(self,mylat,mylon,dist):
		"""return ids of users within dist meters"""
		lat = math.radians(mylat)
		lon = math.radians(mylon)
		stmt = "SELECT id, 6371 * 2 * ASIN(SQRT(POWER(SIN(RADIANS(42 - ABS(locations.lat))), 2) \
			+ COS(RADIANS(42)) * COS(RADIANS(ABS(locations.lat))) * POWER(SIN(RADIANS(12 - locations.lon)), 2))) \
			AS distance FROM locations HAVING distance < 0.5 ORDER BY distance;"
		self.cursor.execute(stmt)
		return self.cursor.fetchall()


	def search_nearby2(self,mylat,mylon,dist):
		"""return ids of users within dist meters"""
		lat = math.radians(mylat)
		lon = math.radians(mylon)

		lon1 = lon - dist / math.fabs(math.cos(lat)*111.04)
		lon2 = lon + dist / math.fabs(math.cos(lat)*111.04)

		lat1 = lat – dist / (111.04)
		lat2 = lat + dist / (111.04)

		stmt = "SELECT id, 6371 * 2 * ASIN(SQRT(POWER(SIN(RADIANS(42 - ABS(locations.lat))), 2) \
			+ COS(RADIANS(42)) * COS(RADIANS(ABS(locations.lat))) * POWER(SIN(RADIANS(12 - locations.lon)), 2))) \
			AS distance FROM locations HAVING distance < 0.5 ORDER BY distance;"
		self.cursor.execute(stmt)
		return self.cursor.fetchall()


	def search_nearby3(self,mylat,mylon,dist):
		"""return ids of users within dist meters"""
		lat = math.radians(mylat)
		lon = math.radians(mylon)
		stmt = "SELECT id, 6371 * 2 * ASIN(SQRT(POWER(SIN(RADIANS(42 - ABS(locations.lat))), 2) \
			+ COS(RADIANS(42)) * COS(RADIANS(ABS(locations.lat))) * POWER(SIN(RADIANS(12 - locations.lon)), 2))) \
			AS distance FROM locations HAVING distance < 0.5 ORDER BY distance;"
		self.cursor.execute(stmt)
		return self.cursor.fetchall()


	def generate_random_places(self,nrows):
		"""generate csvfiles with nrows data points in random locations"""
		data = []
		for i in range(nrows):
			place = [round(random.uniform(-90,90),7),
				round(random.uniform(-180,180),7)]
			data.append(place)


	def generate_gauss_places(self,nrows):
	 	"""simulate dense population data points around lat=42, lon=12"""
		data = []
		for i in range(nrows): 
			place = [round(random.gauss(42,0.05),7),
				round(random.gauss(12,0.05),7)]
			data.append(place) 

		with open('places.csv', 'w') as csvfile:
			f = csv.writer(csvfile)
			f.writerows(data)


	def load_db(self):
		"""bulk import places.csv into db"""
		stmt = "load data local infile 'places.csv' into table locations \
		fields terminated by ',' lines terminated by '\n' (lat, lon)"
		self.cursor.execute(stmt)
		self.db.commit()


	def close_db(self):
		self.db.close()


if __name__ == '__main__':
	DB()
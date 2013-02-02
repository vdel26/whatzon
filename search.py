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
		stmt = "SELECT id, 6371 * 2 * ASIN(SQRT(POWER(SIN(RADIANS(%(0)f - ABS(locations.lat))), 2) \
			+ COS(RADIANS(%(0)f)) * COS(RADIANS(ABS(locations.lat))) * POWER(SIN(RADIANS(%(1)f - locations.lon)), 2))) \
			AS distance FROM locations HAVING distance < %(2)f ORDER BY distance;" %{'0':mylat, '1':mylon, '2':dist}
		self.cursor.execute(stmt)
		return self.cursor.fetchall()


	def search_nearby2(self,mylat,mylon,dist):
		"""return ids of users within dist meters"""
		lon1 = mylon - dist / math.fabs(math.cos(math.radians(mylat))*111.04)
		lon2 = mylon + dist / math.fabs(math.cos(math.radians(mylat))*111.04)

		lat1 = mylat - dist / (111.04)
		lat2 = mylat + dist / (111.04)

		stmt = "SELECT id, 6371 * 2 * ASIN(SQRT(POWER(SIN(RADIANS(%(0)f - ABS(locations.lat))), 2) \
		 + COS(RADIANS(%(0)f)) * COS(RADIANS(ABS(locations.lat))) * POWER(SIN(RADIANS(%(1)f - locations.lon)), 2))) \
		 AS distance FROM locations WHERE locations.lat BETWEEN %(5)f AND %(6)f \
		 AND locations.lon BETWEEN %(3)f AND %(4)f HAVING distance < %(2)f \
		 ORDER BY distance;" %{'0':mylat, '1':mylon, '2':dist, '3':lon1, '4':lon2, '5':lat1, '6':lat2}
		self.cursor.execute(stmt)
		return self.cursor.fetchall()


	def search_nearby3(self,mylat,mylon,dist):
		"""return ids of users within dist meters"""
		lat = math.radians(mylat)
		lon = math.radians(mylon)
		stmt = "SELECT id, 6371 * 2 * ASIN(SQRT(POWER(SIN(RADIANS(%(0)f - ABS(locations.lat))), 2) \
			+ COS(RADIANS(%(0)f)) * COS(RADIANS(ABS(locations.lat))) * POWER(SIN(RADIANS(%(1)f - locations.lon)), 2))) \
			AS distance FROM locations HAVING distance < %(2)f ORDER BY distance;" %{'0':lat, '1':lon, '2':dist}
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
	print "import as module and instatiate DB object."
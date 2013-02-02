#query 1
SELECT id, 6371 * 2 * ASIN(SQRT(POWER(SIN(RADIANS(42 - ABS(locations.lat))), 2) + COS(RADIANS(42)) * COS(RADIANS(ABS(locations.lat))) * POWER(SIN(RADIANS(12 - locations.lon)), 2))) AS distance FROM locations HAVING distance < 1 ORDER BY distance LIMIT 10;


SELECT id, 6371 * 2 * ASIN(SQRT(POWER(SIN(RADIANS(42.000000 - ABS(locations.lat))), 2) + COS(RADIANS(42.000000)) * COS(RADIANS(ABS(locations.lat))) * POWER(SIN(RADIANS(12.000000 - locations.lon)), 2))) AS distance FROM locations HAVING distance < 0.500000 ORDER BY distance;


#query 2
###primero definir indices en lat y long  
CREATE INDEX `index_places_on_latitude_and_longitude` ON `locations` (`lat`, `lon`)

###calcular rectángulo que limita
long1 = orig.long – dist / ABS(COS(RADIANS(orig.lat)) * 111.04)
long2 = orig.long + dist / ABS(COS(RADIANS(orig.lat)) * 111.04)

lat1 = orig.lat – dist / (111.04)
lat2 = orig.lat + dist / (111.04)

###query
SELECT id,
6371 * 2 * ASIN(SQRT(POWER(SIN(RADIANS(orig.lat - ABS(locations.lat))), 2) + COS(RADIANS(orig.lat)) * COS(RADIANS(ABS(locations.lat))) * POWER(SIN(RADIANS(orig.lon - locations.lon)), 2))) AS distance
FROM locations
WHERE locations.lat BETWEEN lat1 AND lat2 AND locations.lon BETWEEN lon1 AND lon2
HAVING distance < 10
ORDER BY distance;

#query3

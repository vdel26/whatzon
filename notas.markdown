#query 1
SELECT id, 6371 * 2 * ASIN(SQRT(POWER(SIN(RADIANS(42 - ABS(locations.lat))), 2) + COS(RADIANS(42)) * COS(RADIANS(ABS(locations.lat))) * POWER(SIN(RADIANS(12 - locations.lon)), 2))) AS distance FROM locations HAVING distance < 1 ORDER BY distance LIMIT 10;

#query2 (primero definir indices en lat y long)
CREATE INDEX `index_places_on_latitude_and_longitude` ON `locations` (`lat`, `lon`)

# MODO 1
### query (ejemplo: lat=42, lon=12, dist = 0.5km)
SELECT id, 6371 * 2 * ASIN(SQRT(POWER(SIN(RADIANS(42.000000 - ABS(locations.lat))), 2) + COS(RADIANS(42.000000)) * COS(RADIANS(ABS(locations.lat))) * POWER(SIN(RADIANS(12.000000 - locations.lon)), 2))) AS distance FROM locations HAVING distance < 0.500000 ORDER BY distance;


# MODO 2
### primero definir indices en lat y long  
CREATE INDEX `index_places_on_latitude_and_longitude` ON `locations` (`lat`, `lon`)

### calcular rectángulo que limita
long1 = orig.long – dist / ABS(COS(RADIANS(orig.lat)) * 111.04)
long2 = orig.long + dist / ABS(COS(RADIANS(orig.lat)) * 111.04)

lat1 = orig.lat – dist / (111.04)
lat2 = orig.lat + dist / (111.04)

### query (ejemplo: lat=42, lon=12, dist = 0.5km)
SELECT id, 6371 * 2 * ASIN(SQRT(POWER(SIN(RADIANS(42 - ABS(locations.lat))), 2) + COS(RADIANS(42)) * COS(RADIANS(ABS(locations.lat))) * POWER(SIN(RADIANS(12 - locations.lon)), 2))) AS distance
FROM locations
WHERE locations.lat BETWEEN 41.99549711815562 AND 42.00450288184438 AND locations.lon BETWEEN 11.993940774812652 AND 12.006059225187348
HAVING distance < 0.5
ORDER BY distance;


In [14]: lon1
11.993940774812652

In [16]: lon2
12.006059225187348

In [18]: lat1
41.99549711815562

In [20]: lat2
42.00450288184438


# MODO 3
### crear campo de datos espacial
ALTER TABLE locations ADD position POINT NOT NULL;
UPDATE locations SET position = POINT(locations.lat, locations.lon);
ALTER TABLE locations ADD SPATIAL KEY (position);

*notas:*    
1. El motor tiene que ser MyISAM para poder soportar índices espaciales
2. Las posiciones tienen que estar cargadas en la DB antes de añadir la columna 'position'

### crear funcion distancia
DELIMITER $$
 CREATE FUNCTION distance (a POINT, b POINT) RETURNS double DETERMINISTIC
   BEGIN
     RETURN 6371 * 2 * ASIN(SQRT(POWER(SIN(RADIANS(ABS(X(a)) - ABS(X(b)))), 2) + COS(RADIANS(ABS(X(a)))) * COS(RADIANS(ABS(X(b)))) * POWER(SIN(RADIANS(Y(a) - Y(b))), 2)));
   END  $$
DELIMITER;

### definir polígono (como tenemos tipo de datos POINT podemos usar la siguiente función)
SET @bbox = 'POLYGON((lat1 lon1, lat1 lon2, lat2 lon2, lat2 lon1, lat1 lon1))'

*ejemplo*  
SET @bbox = 'POLYGON((41.99549711815562 11.993940774812652, 41.99549711815562 12.006059225187348,42.00450288184438 12.006059225187348, 42.00450288184438 11.993940774812652, 41.99549711815562 11.993940774812652))';

### query (ejemplo: lat=42, lon=12, dist = 0.5km)  
SELECT id, distance(locations.position, POINT(42, 12)) AS cdist
FROM locations
WHERE INTERSECTS(locations.position, PolygonFromText(@bbox))
HAVING cdist < 0.5
ORDER BY cdist;


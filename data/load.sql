LOAD DATA INFILE '/var/lib/mysql-files/track_points.csv' 
INTO TABLE track 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'

CREATE TABLE `sensor_id3` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `distance_error` float DEFAULT NULL,
  `measure` float DEFAULT NULL,
  `sensed` datetime DEFAULT CURRENT_TIMESTAMP,
  `lon` float DEFAULT NULL,
  `lat` float DEFAULT NULL,
  UNIQUE KEY `id` (`id`)
)

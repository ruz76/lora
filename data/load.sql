CREATE TABLE `gtws` (
  `id` int(11) NOT NULL,
  `mqttid` varchar(50) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  `x` int(11) DEFAULT NULL,
  `y` int(11) DEFAULT NULL,
  `lon` float DEFAULT NULL,
  `lat` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOAD DATA INFILE '/var/lib/mysql-files/gtws.csv'
INTO TABLE gtws
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

CREATE TABLE `track` (
  `id` int(11) DEFAULT NULL,
  `lon` float DEFAULT NULL,
  `lat` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOAD DATA INFILE '/var/lib/mysql-files/track_points.csv'
INTO TABLE track 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

CREATE TABLE `sensors` (
  `id` int(11) NOT NULL,
  `mqttid` varchar(50) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  `description` varchar(50) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `x` int(11) DEFAULT NULL,
  `y` int(11) DEFAULT NULL,
  `lon` float DEFAULT NULL,
  `lat` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOAD DATA INFILE '/var/lib/mysql-files/sensors.csv'
INTO TABLE sensors
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

CREATE TABLE `sensor_id1` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `distance_error` float DEFAULT NULL,
  `measure` float DEFAULT NULL,
  `sensed` datetime DEFAULT CURRENT_TIMESTAMP,
  `lon` float DEFAULT NULL,
  `lat` float DEFAULT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE `sensor_id2` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `distance_error` float DEFAULT NULL,
  `measure` float DEFAULT NULL,
  `sensed` datetime DEFAULT CURRENT_TIMESTAMP,
  `lon` float DEFAULT NULL,
  `lat` float DEFAULT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE `sensor_id3` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `distance_error` float DEFAULT NULL,
  `measure` float DEFAULT NULL,
  `sensed` datetime DEFAULT CURRENT_TIMESTAMP,
  `lon` float DEFAULT NULL,
  `lat` float DEFAULT NULL,
  `lastid` int(11) DEFAULT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5887 DEFAULT CHARSET=latin1;

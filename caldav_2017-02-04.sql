# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.17)
# Database: caldav
# Generation Time: 2017-02-04 08:16:08 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table ACCOUNT
# ------------------------------------------------------------

DROP TABLE IF EXISTS `ACCOUNT`;

CREATE TABLE `ACCOUNT` (
  `host_name` varchar(200) NOT NULL DEFAULT '',
  `user_id` varchar(30) NOT NULL DEFAULT '',
  `user_base64` varchar(512) DEFAULT '',
  `home_set_cal_url` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`host_name`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `ACCOUNT` WRITE;
/*!40000 ALTER TABLE `ACCOUNT` DISABLE KEYS */;

INSERT INTO `ACCOUNT` (`host_name`, `user_id`, `user_base64`, `home_set_cal_url`)
VALUES
	('https://caldav.calendar.naver.com/principals/users/jspiner','jspiner','navera4515780145','/caldav/jspiner/calendar/');

/*!40000 ALTER TABLE `ACCOUNT` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table CALENDAR
# ------------------------------------------------------------

DROP TABLE IF EXISTS `CALENDAR`;

CREATE TABLE `CALENDAR` (
  `host_name` varchar(200) NOT NULL DEFAULT '',
  `user_id` varchar(30) NOT NULL DEFAULT '',
  `calendar_id` varchar(256) NOT NULL DEFAULT '',
  `calendar_url` varchar(512) DEFAULT '',
  `calendar_name` varchar(64) DEFAULT '',
  `c_tag` varchar(512) DEFAULT '',
  PRIMARY KEY (`host_name`,`user_id`,`calendar_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table EVENT
# ------------------------------------------------------------

DROP TABLE IF EXISTS `EVENT`;

CREATE TABLE `EVENT` (
  `host_name` varchar(200) NOT NULL DEFAULT '',
  `user_id` varchar(30) NOT NULL DEFAULT '',
  `calendar_id` varchar(256) NOT NULL DEFAULT '',
  `event_id` varchar(256) NOT NULL DEFAULT '',
  `event_url` varchar(512) DEFAULT '',
  `e_tag` varchar(512) DEFAULT '',
  `start_dt` datetime DEFAULT NULL,
  `end_dt` datetime DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`host_name`,`user_id`,`calendar_id`,`event_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

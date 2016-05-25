-- MySQL dump 10.13  Distrib 5.5.49, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: cameras
-- ------------------------------------------------------
-- Server version	5.5.49-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `camera`
--

DROP TABLE IF EXISTS `camera`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camera` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=138340 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camera`
--

LOCK TABLES `camera` WRITE;
/*!40000 ALTER TABLE `camera` DISABLE KEYS */;
INSERT INTO `camera` VALUES (23),(24),(25),(28),(79),(673),(857),(918),(1023),(3899),(3908),(31763),(31764),(31766),(31768),(31771),(32402),(32403),(32404),(44820);
/*!40000 ALTER TABLE `camera` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ip_camera`
--

DROP TABLE IF EXISTS `ip_camera`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ip_camera` (
  `camera_id` int(10) unsigned NOT NULL,
  `ip` varchar(44) NOT NULL,
  `port` int(11) DEFAULT NULL,
  `ip_camera_model_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`camera_id`),
  KEY `ip_camera_model_id` (`ip_camera_model_id`),
  CONSTRAINT `ip_camera_ibfk_1` FOREIGN KEY (`camera_id`) REFERENCES `camera` (`id`),
  CONSTRAINT `ip_camera_ibfk_2` FOREIGN KEY (`ip_camera_model_id`) REFERENCES `ip_camera_model` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ip_camera`
--

LOCK TABLES `ip_camera` WRITE;
/*!40000 ALTER TABLE `ip_camera` DISABLE KEYS */;
INSERT INTO `ip_camera` VALUES (23,'128.10.29.31',NULL,11),(24,'128.10.29.32',NULL,11),(25,'128.10.29.33',NULL,11),(28,'128.104.181.37',NULL,11),(79,'128.210.129.12',NULL,11),(673,'217.91.58.189',1024,11),(857,'140.232.203.246',NULL,11),(918,'69.18.18.82',NULL,11),(1023,'66.231.56.22',NULL,11),(44820,'198.82.159.134',NULL,11);
/*!40000 ALTER TABLE `ip_camera` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ip_camera_model`
--

DROP TABLE IF EXISTS `ip_camera_model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ip_camera_model` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `brand` varchar(50) DEFAULT NULL,
  `video_path` varchar(100) DEFAULT NULL,
  `image_path` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`brand`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ip_camera_model`
--

LOCK TABLES `ip_camera_model` WRITE;
/*!40000 ALTER TABLE `ip_camera_model` DISABLE KEYS */;
INSERT INTO `ip_camera_model` VALUES (11,'Axis','/axis-cgi/mjpg/video.cgi','/axis-cgi/jpg/image.cgi');
/*!40000 ALTER TABLE `ip_camera_model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `non_ip_camera`
--

DROP TABLE IF EXISTS `non_ip_camera`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `non_ip_camera` (
  `camera_id` int(10) unsigned NOT NULL,
  `snapshot_url` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`camera_id`),
  UNIQUE KEY `snapshot_url` (`snapshot_url`),
  CONSTRAINT `non_ip_camera_ibfk_1` FOREIGN KEY (`camera_id`) REFERENCES `camera` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `non_ip_camera`
--

LOCK TABLES `non_ip_camera` WRITE;
/*!40000 ALTER TABLE `non_ip_camera` DISABLE KEYS */;
INSERT INTO `non_ip_camera` VALUES (31763,'http://207.251.86.238/cctv10.jpg'),(31764,'http://207.251.86.238/cctv106.jpg'),(31766,'http://207.251.86.238/cctv11.jpg'),(31768,'http://207.251.86.238/cctv114.jpg'),(31771,'http://207.251.86.238/cctv12.jpg'),(32402,'http://cmhimg01.dot.state.oh.us/images/artimis/CCTV001a-L.jpg'),(32403,'http://cmhimg01.dot.state.oh.us/images/artimis/CCTV002a-L.jpg'),(32404,'http://cmhimg01.dot.state.oh.us/images/artimis/CCTV003a-L.jpg'),(3899,'http://images.webcams.travel/preview/1168708590.jpg'),(3908,'http://images.webcams.travel/preview/1170678944.jpg');
/*!40000 ALTER TABLE `non_ip_camera` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-05-16 22:41:12

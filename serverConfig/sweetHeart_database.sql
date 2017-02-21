-- MySQL dump 10.13  Distrib 5.7.17, for Linux (x86_64)
--
-- Host: localhost    Database: SweetHeart
-- ------------------------------------------------------
-- Server version	5.7.17-0ubuntu0.16.04.1

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('0570c26200d0');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cakes`
--

DROP TABLE IF EXISTS `cakes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cakes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `desc` varchar(100) NOT NULL,
  `detail` varchar(200) DEFAULT NULL,
  `price` decimal(8,2) NOT NULL,
  `imgUrl` varchar(100) NOT NULL,
  `orders` int(11) DEFAULT NULL,
  `stars` int(11) DEFAULT NULL,
  `cateId` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `cateId` (`cateId`),
  CONSTRAINT `cakes_ibfk_1` FOREIGN KEY (`cateId`) REFERENCES `categories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cakes`
--

LOCK TABLES `cakes` WRITE;
/*!40000 ALTER TABLE `cakes` DISABLE KEYS */;
INSERT INTO `cakes` VALUES (11,'creamCake','鲜奶蛋糕','这是鲜奶蛋糕',58.00,'creamCake.jpg',0,3,1),(12,'fruitCake','水果蛋糕','这是水果蛋糕',58.00,'fruitCake.jpg',0,3,1),(13,'personalCake','个性蛋糕','这是个性蛋糕',118.00,'personalCake.jpg',0,3,1),(14,'mousseCake','慕斯蛋糕','这是慕斯蛋糕',78.00,'mousseCake.jpg',0,3,1),(15,'flowerCake','鲜花蛋糕','这是鲜花蛋糕',78.00,'flowerCake.jpg',0,3,1),(16,'layerCake','千层蛋糕','这是千层蛋糕',128.00,'layerCake.jpg',0,3,1),(17,'paperCake','纸杯蛋糕','这是纸杯蛋糕',32.80,'paperCake.jpg',0,3,1),(21,'cookies','曲奇饼干','这是曲奇饼干',32.80,'cookies.jpg',0,3,2),(22,'Marguerite','玛格丽特','这是玛格丽特，一点都不像饼干的名字',32.80,'Marguerite.jpg',0,3,2),(23,'cartoonCookies','卡通饼干','这是卡通饼干',32.80,'cartoonCookies.jpg',0,3,2),(24,'cranberryCookies','蔓越莓饼干','这是蔓越莓饼干，一点都不像饼干的名字',32.80,'cranberryCookies.jpg',0,3,2),(25,'xlkq','昔腊可球','这是昔腊可球',32.80,'xlkq.jpg',0,3,2),(31,'creamPudding','奶油布丁','这是奶油布丁',32.80,'creamPudding.jpg',0,3,3),(32,'mangoPudding','芒果布丁','这是芒果布丁',32.80,'mangoPudding.jpg',0,3,3),(33,'strawberryPudding','草莓布丁','这是草莓布丁',32.80,'strawberryPudding.jpg',0,3,3),(34,'blueberryPudding','蓝莓布丁','这是蓝莓布丁',32.80,'blueberryPudding.jpg',0,3,3),(41,'strawberryChocolate','草莓味巧克力','这是草莓味巧克力',32.80,'strawberryChocolate.jpg',0,3,4),(42,'lemonChocolate','柠檬味巧克力','这是柠檬味巧克力',32.80,'lemonChocolate.jpg',0,3,4),(43,'matchaChocolate','抹茶味巧克力','这是抹茶味巧克力',32.80,'matchaChocolate.jpg',0,3,4),(44,'whiteMilkChocolate','白牛奶味巧克力','这是白牛奶味巧克力',32.80,'whiteMilkChocolate.jpg',0,3,4),(45,'bitterSweetChocolate','苦甜味巧克力','这是苦甜味巧克力',32.80,'bitterSweetChocolate.jpg',0,3,4);
/*!40000 ALTER TABLE `cakes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `desc` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'cake','蛋糕'),(2,'biscuit','饼干'),(3,'pudding','布丁'),(4,'chocolate','巧克力');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `openId` varchar(50) NOT NULL,
  `nickName` varchar(100) NOT NULL,
  `gender` int(11) DEFAULT NULL,
  `city` varchar(40) DEFAULT NULL,
  `province` varchar(40) DEFAULT NULL,
  `country` varchar(40) DEFAULT NULL,
  `avatarUrl` varchar(100) DEFAULT NULL,
  `unionId` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `openId` (`openId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-02-14 19:19:55

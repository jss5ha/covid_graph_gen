-- MySQL dump 10.14  Distrib 5.5.60-MariaDB, for Linux (x86_64)
--
-- Host: usersrv01.cs.virginia.edu    Database: twittertnet
-- ------------------------------------------------------
-- Server version	8.0.20

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
-- Table structure for table `HydraScriptTestTable`
--

DROP TABLE IF EXISTS `HydraScriptTestTable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HydraScriptTestTable` (
  `tweetid` bigint DEFAULT NULL,
  `userid` bigint DEFAULT NULL,
  `text` text,
  `created_at` datetime DEFAULT NULL,
  `entities` text,
  `language` varchar(5) DEFAULT NULL,
  `retweet_id` bigint DEFAULT NULL,
  `retweet_userid` bigint DEFAULT NULL,
  `conversation_id` bigint DEFAULT NULL,
  KEY `userid_idx` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hashtags`
--

DROP TABLE IF EXISTS `hashtags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hashtags` (
  `id` int NOT NULL AUTO_INCREMENT,
  `hashtag` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hashindex` (`hashtag`)
) ENGINE=InnoDB AUTO_INCREMENT=52890394 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `masktweets`
--

DROP TABLE IF EXISTS `masktweets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `masktweets` (
  `tweetid` bigint NOT NULL,
  `userid` bigint DEFAULT NULL,
  `text` text,
  `created_at` datetime DEFAULT NULL,
  `entities` text,
  `language` varchar(5) DEFAULT NULL,
  `retweet_id` bigint DEFAULT NULL,
  `retweet_userid` bigint DEFAULT NULL,
  `conversation_id` bigint DEFAULT NULL,
  `sentiment` double DEFAULT NULL,
  PRIMARY KEY (`tweetid`),
  KEY `userid_idx` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mentions`
--

DROP TABLE IF EXISTS `mentions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mentions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tweetid` bigint DEFAULT NULL,
  `userid` bigint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=114490889 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `retweet`
--

DROP TABLE IF EXISTS `retweet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `retweet` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tweetid` bigint DEFAULT NULL,
  `originalid` bigint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=113192192 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `test_table`
--

DROP TABLE IF EXISTS `test_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `test_table` (
  `tweetid` bigint NOT NULL,
  `userid` bigint DEFAULT NULL,
  `text` text,
  `created_at` datetime DEFAULT NULL,
  `entities` text,
  `language` varchar(5) DEFAULT NULL,
  `retweet_id` bigint DEFAULT NULL,
  `retweet_userid` bigint DEFAULT NULL,
  `conversation_id` bigint DEFAULT NULL,
  PRIMARY KEY (`tweetid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `testtable`
--

DROP TABLE IF EXISTS `testtable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `testtable` (
  `tweetid` bigint NOT NULL,
  `userid` bigint DEFAULT NULL,
  `text` varchar(280) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`tweetid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tweet_hashtag`
--

DROP TABLE IF EXISTS `tweet_hashtag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tweet_hashtag` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tweetid` bigint NOT NULL,
  `hashtagid` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tweetid` (`tweetid`)
) ENGINE=InnoDB AUTO_INCREMENT=50955490 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tweets`
--

DROP TABLE IF EXISTS `tweets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tweets` (
  `tweetid` bigint NOT NULL,
  `userid` bigint DEFAULT NULL,
  `text` text,
  `created_at` datetime DEFAULT NULL,
  `entities` text,
  `language` varchar(5) DEFAULT NULL,
  `retweet_id` bigint DEFAULT NULL,
  `retweet_userid` bigint DEFAULT NULL,
  `conversation_id` bigint DEFAULT NULL,
  PRIMARY KEY (`tweetid`),
  KEY `userid_idx` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-13  1:28:32

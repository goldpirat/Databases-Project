/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.9-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: kflori_db
-- ------------------------------------------------------
-- Server version	10.11.9-MariaDB-ubu2404

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Account_Management`
--

DROP TABLE IF EXISTS `Account_Management`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Account_Management` (
  `Account_ID` int(11) NOT NULL AUTO_INCREMENT,
  `User_ID` int(11) DEFAULT NULL,
  `Profile_Edit_Date` date DEFAULT NULL,
  PRIMARY KEY (`Account_ID`),
  KEY `User_ID` (`User_ID`),
  CONSTRAINT `Account_Management_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `User` (`User_ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Account_Management`
--

LOCK TABLES `Account_Management` WRITE;
/*!40000 ALTER TABLE `Account_Management` DISABLE KEYS */;
/*!40000 ALTER TABLE `Account_Management` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Book`
--

DROP TABLE IF EXISTS `Book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Book` (
  `Book_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Title` varchar(255) NOT NULL,
  `Author` varchar(255) DEFAULT NULL,
  `ISBN` varchar(13) DEFAULT NULL,
  `Available_Copies` int(11) DEFAULT 1 CHECK (`Available_Copies` >= 0),
  PRIMARY KEY (`Book_ID`),
  UNIQUE KEY `ISBN` (`ISBN`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Book`
--

LOCK TABLES `Book` WRITE;
/*!40000 ALTER TABLE `Book` DISABLE KEYS */;
INSERT INTO `Book` VALUES
(1,'48 Laws of Power','Robert Greene','9780140280197',2),
(2,'Little Red Riding Hood (Keepsake Stories)','N/A','9781577681984',15),
(3,'Moby Dick (Wordsworth Classics)','Melville Herman','9781853260087',7),
(4,'The Bro Code','Barney Stinson - Matt Kuhn','9781439110003',32),
(5,'The Kite Runner','Khaled Hosseini','9781594631931',14),
(6,'The Laws of Human Nature','Robert Greene','9781781259191',8),
(7,'The Witness','Sandra Brown','9781455538263',7),
(8,'The Old Man and The Sea','Ernest Hemingway','9798329875195',5),
(9,'The 7 Habits of Highly Effective People: 30th Anniversary Edition','Stephen R. Covey','781982137274',4);
/*!40000 ALTER TABLE `Book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Borrowing`
--

DROP TABLE IF EXISTS `Borrowing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Borrowing` (
  `Borrowing_ID` int(11) NOT NULL AUTO_INCREMENT,
  `User_ID` int(11) DEFAULT NULL,
  `Book_ID` int(11) DEFAULT NULL,
  `Borrow_Date` date NOT NULL,
  `Return_Date` date DEFAULT NULL,
  `Status` enum('Borrowed','Returned') DEFAULT 'Borrowed',
  PRIMARY KEY (`Borrowing_ID`),
  KEY `User_ID` (`User_ID`),
  KEY `Book_ID` (`Book_ID`),
  CONSTRAINT `Borrowing_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `User` (`User_ID`) ON DELETE CASCADE,
  CONSTRAINT `Borrowing_ibfk_2` FOREIGN KEY (`Book_ID`) REFERENCES `Book` (`Book_ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Borrowing`
--

LOCK TABLES `Borrowing` WRITE;
/*!40000 ALTER TABLE `Borrowing` DISABLE KEYS */;
INSERT INTO `Borrowing` VALUES
(1,3,2,'2024-09-20','2024-09-24','Returned'),
(2,6,2,'2024-09-14','2024-09-19','Returned'),
(3,6,4,'2024-09-20','2024-09-24','Returned'),
(4,4,8,'2024-09-20','2024-09-24','Returned'),
(5,2,9,'2024-09-22','2024-09-23','Returned'),
(6,5,7,'2024-09-22','2024-09-23','Returned'),
(7,3,9,'2024-09-10','2024-09-12','Returned'),
(8,4,1,'2024-09-18','2024-09-23','Returned');
/*!40000 ALTER TABLE `Borrowing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Librarian`
--

DROP TABLE IF EXISTS `Librarian`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Librarian` (
  `User_ID` int(11) NOT NULL,
  PRIMARY KEY (`User_ID`),
  CONSTRAINT `Librarian_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `User` (`User_ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Librarian`
--

LOCK TABLES `Librarian` WRITE;
/*!40000 ALTER TABLE `Librarian` DISABLE KEYS */;
INSERT INTO `Librarian` VALUES
(1);
/*!40000 ALTER TABLE `Librarian` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Regular_User`
--

DROP TABLE IF EXISTS `Regular_User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Regular_User` (
  `User_ID` int(11) NOT NULL,
  PRIMARY KEY (`User_ID`),
  CONSTRAINT `Regular_User_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `User` (`User_ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Regular_User`
--

LOCK TABLES `Regular_User` WRITE;
/*!40000 ALTER TABLE `Regular_User` DISABLE KEYS */;
INSERT INTO `Regular_User` VALUES
(2),
(3),
(4),
(5),
(6);
/*!40000 ALTER TABLE `Regular_User` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Reservation`
--

DROP TABLE IF EXISTS `Reservation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Reservation` (
  `Reservation_ID` int(11) NOT NULL AUTO_INCREMENT,
  `User_ID` int(11) DEFAULT NULL,
  `Book_ID` int(11) DEFAULT NULL,
  `Reservation_Date` date NOT NULL,
  `Status` enum('Active','Completed') DEFAULT 'Active',
  PRIMARY KEY (`Reservation_ID`),
  KEY `User_ID` (`User_ID`),
  KEY `Book_ID` (`Book_ID`),
  CONSTRAINT `Reservation_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `User` (`User_ID`) ON DELETE CASCADE,
  CONSTRAINT `Reservation_ibfk_2` FOREIGN KEY (`Book_ID`) REFERENCES `Book` (`Book_ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Reservation`
--

LOCK TABLES `Reservation` WRITE;
/*!40000 ALTER TABLE `Reservation` DISABLE KEYS */;
INSERT INTO `Reservation` VALUES
(1,6,1,'2024-09-20','Active'),
(2,3,5,'2024-09-20','Active');
/*!40000 ALTER TABLE `Reservation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Review`
--

DROP TABLE IF EXISTS `Review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Review` (
  `Review_ID` int(11) NOT NULL AUTO_INCREMENT,
  `User_ID` int(11) DEFAULT NULL,
  `Book_ID` int(11) DEFAULT NULL,
  `Review_Text` text DEFAULT NULL,
  `Rating` int(11) DEFAULT NULL CHECK (`Rating` between 1 and 5),
  `Review_Date` date NOT NULL,
  PRIMARY KEY (`Review_ID`),
  UNIQUE KEY `User_ID` (`User_ID`,`Book_ID`),
  KEY `Book_ID` (`Book_ID`),
  CONSTRAINT `Review_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `User` (`User_ID`) ON DELETE CASCADE,
  CONSTRAINT `Review_ibfk_2` FOREIGN KEY (`Book_ID`) REFERENCES `Book` (`Book_ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Review`
--

LOCK TABLES `Review` WRITE;
/*!40000 ALTER TABLE `Review` DISABLE KEYS */;
INSERT INTO `Review` VALUES
(1,3,2,'Amazing kid`s book!',5,'2024-09-25'),
(2,6,2,'Great for Kids',4,'2024-09-20'),
(3,6,4,'Hilarious!',5,'2024-09-25'),
(4,4,8,'Very Good!',5,'2024-09-25'),
(5,2,9,'Boring!',3,'2024-09-25'),
(6,5,7,'Great writing but some plot holes!',4,'2024-09-25'),
(7,3,9,'Very Helpful!',5,'2024-09-25'),
(8,4,1,'This was very good writing!',5,'2024-09-25');
/*!40000 ALTER TABLE `Review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User` (
  `User_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `Email` varchar(255) NOT NULL,
  PRIMARY KEY (`User_ID`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES
(1,'Flori Kusari','fkusari@constructor.university'),
(2,'Rron Dermaku','rdermaku@constructor.university'),
(3,'Hannah Paulus','hpaulus@constructor.university'),
(4,'Edin Berisha','eberisha@constructor.university'),
(5,'Camila Pina Pinto','cpinto@constructor.university'),
(6,'Lis Fazliu','lfazliu@constructor.university');
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-26 17:54:57

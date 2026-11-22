-- MySQL dump 10.13  Distrib 8.4.10, for Linux (x86_64)
--
-- Host: localhost    Database: cyber_investigation
-- ------------------------------------------------------
-- Server version	8.4.10

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Alert_Logs`
--

DROP TABLE IF EXISTS `Alert_Logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Alert_Logs` (
  `alert_log_id` int NOT NULL AUTO_INCREMENT,
  `alert_id` int NOT NULL,
  `action` varchar(100) NOT NULL,
  `details` text,
  `logged_at` datetime NOT NULL,
  PRIMARY KEY (`alert_log_id`),
  KEY `alert_id` (`alert_id`),
  CONSTRAINT `Alert_Logs_ibfk_1` FOREIGN KEY (`alert_id`) REFERENCES `Alerts` (`alert_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Alerts`
--

DROP TABLE IF EXISTS `Alerts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Alerts` (
  `alert_id` int NOT NULL AUTO_INCREMENT,
  `incident_id` int DEFAULT NULL,
  `ip_id` int DEFAULT NULL,
  `alert_type` varchar(100) NOT NULL,
  `severity` enum('Low','Medium','High','Critical') NOT NULL,
  `detected_at` datetime NOT NULL,
  PRIMARY KEY (`alert_id`),
  KEY `incident_id` (`incident_id`),
  KEY `ip_id` (`ip_id`),
  KEY `idx_alert_detected_at` (`detected_at`),
  CONSTRAINT `Alerts_ibfk_1` FOREIGN KEY (`incident_id`) REFERENCES `Incidents` (`incident_id`),
  CONSTRAINT `Alerts_ibfk_2` FOREIGN KEY (`ip_id`) REFERENCES `IP_Addresses` (`ip_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_alert_log` AFTER INSERT ON `Alerts` FOR EACH ROW BEGIN
    INSERT INTO Alert_Logs
    (alert_id, action, details, logged_at)
    VALUES
    (
        NEW.alert_id,
        'Alert Created',
        CONCAT('Automatically generated ', NEW.severity, ' severity alert'),
        NOW()
    );
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Temporary view structure for view `Critical_Incident_Report`
--

DROP TABLE IF EXISTS `Critical_Incident_Report`;
/*!50001 DROP VIEW IF EXISTS `Critical_Incident_Report`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `Critical_Incident_Report` AS SELECT 
 1 AS `incident_id`,
 1 AS `incident_type`,
 1 AS `severity`,
 1 AS `status`,
 1 AS `reported_at`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `Devices`
--

DROP TABLE IF EXISTS `Devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Devices` (
  `device_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `device_name` varchar(100) NOT NULL,
  `device_type` varchar(50) NOT NULL,
  `operating_system` varchar(50) NOT NULL,
  PRIMARY KEY (`device_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `Devices_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Evidence`
--

DROP TABLE IF EXISTS `Evidence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Evidence` (
  `evidence_id` int NOT NULL AUTO_INCREMENT,
  `incident_id` int NOT NULL,
  `evidence_type` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `collected_at` datetime NOT NULL,
  `file_reference` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`evidence_id`),
  KEY `incident_id` (`incident_id`),
  CONSTRAINT `Evidence_ibfk_1` FOREIGN KEY (`incident_id`) REFERENCES `Incidents` (`incident_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `IP_Addresses`
--

DROP TABLE IF EXISTS `IP_Addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `IP_Addresses` (
  `ip_id` int NOT NULL AUTO_INCREMENT,
  `ip_address` varchar(45) NOT NULL,
  `ip_type` enum('Internal','External') NOT NULL,
  `location` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`ip_id`),
  UNIQUE KEY `ip_address` (`ip_address`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `Incident_Report`
--

DROP TABLE IF EXISTS `Incident_Report`;
/*!50001 DROP VIEW IF EXISTS `Incident_Report`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `Incident_Report` AS SELECT 
 1 AS `incident_id`,
 1 AS `affected_user`,
 1 AS `device_name`,
 1 AS `device_type`,
 1 AS `incident_type`,
 1 AS `description`,
 1 AS `severity`,
 1 AS `status`,
 1 AS `investigator`,
 1 AS `reported_at`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `Incident_Status_History`
--

DROP TABLE IF EXISTS `Incident_Status_History`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Incident_Status_History` (
  `history_id` int NOT NULL AUTO_INCREMENT,
  `incident_id` int NOT NULL,
  `old_status` varchar(30) DEFAULT NULL,
  `new_status` varchar(30) NOT NULL,
  `changed_at` datetime NOT NULL,
  PRIMARY KEY (`history_id`),
  KEY `incident_id` (`incident_id`),
  CONSTRAINT `Incident_Status_History_ibfk_1` FOREIGN KEY (`incident_id`) REFERENCES `Incidents` (`incident_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Incidents`
--

DROP TABLE IF EXISTS `Incidents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Incidents` (
  `incident_id` int NOT NULL AUTO_INCREMENT,
  `device_id` int NOT NULL,
  `investigator_id` int DEFAULT NULL,
  `incident_type` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `severity` enum('Low','Medium','High','Critical','Unassigned') NOT NULL DEFAULT 'Unassigned',
  `status` enum('Open','Under Investigation','Resolved','Closed','Pending Assessment') NOT NULL DEFAULT 'Pending Assessment',
  `reported_at` datetime NOT NULL,
  PRIMARY KEY (`incident_id`),
  KEY `device_id` (`device_id`),
  KEY `investigator_id` (`investigator_id`),
  KEY `idx_incident_severity` (`severity`),
  KEY `idx_incident_status` (`status`),
  KEY `idx_incident_reported_at` (`reported_at`),
  CONSTRAINT `Incidents_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `Devices` (`device_id`),
  CONSTRAINT `Incidents_ibfk_2` FOREIGN KEY (`investigator_id`) REFERENCES `Investigators` (`investigator_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_generate_alert` AFTER INSERT ON `Incidents` FOR EACH ROW BEGIN
    IF NEW.severity IN ('High', 'Critical') THEN

        INSERT INTO Alerts
        (incident_id, ip_id, alert_type, severity, detected_at)
        VALUES
        (
            NEW.incident_id,
            NULL,
            CONCAT(NEW.severity, ' Severity Incident'),
            NEW.severity,
            NEW.reported_at
        );

    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_initial_status_history` AFTER INSERT ON `Incidents` FOR EACH ROW BEGIN
    INSERT INTO Incident_Status_History
    (incident_id, old_status, new_status, changed_at)
    VALUES
    (
        NEW.incident_id,
        NULL,
        NEW.status,
        NOW()
    );
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_status_change` AFTER UPDATE ON `Incidents` FOR EACH ROW BEGIN
    IF OLD.status <> NEW.status THEN

        INSERT INTO Incident_Status_History
        (incident_id, old_status, new_status, changed_at)
        VALUES
        (
            NEW.incident_id,
            OLD.status,
            NEW.status,
            NOW()
        );

    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `Investigation_Logs`
--

DROP TABLE IF EXISTS `Investigation_Logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Investigation_Logs` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `incident_id` int NOT NULL,
  `investigator_id` int NOT NULL,
  `action_performed` text NOT NULL,
  `action_timestamp` datetime NOT NULL,
  PRIMARY KEY (`log_id`),
  KEY `incident_id` (`incident_id`),
  KEY `investigator_id` (`investigator_id`),
  KEY `idx_investigation_timestamp` (`action_timestamp`),
  CONSTRAINT `Investigation_Logs_ibfk_1` FOREIGN KEY (`incident_id`) REFERENCES `Incidents` (`incident_id`),
  CONSTRAINT `Investigation_Logs_ibfk_2` FOREIGN KEY (`investigator_id`) REFERENCES `Investigators` (`investigator_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `Investigator_Workload_Report`
--

DROP TABLE IF EXISTS `Investigator_Workload_Report`;
/*!50001 DROP VIEW IF EXISTS `Investigator_Workload_Report`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `Investigator_Workload_Report` AS SELECT 
 1 AS `investigator_id`,
 1 AS `investigator_name`,
 1 AS `role`,
 1 AS `total_incidents`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `Investigators`
--

DROP TABLE IF EXISTS `Investigators`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Investigators` (
  `investigator_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `role` varchar(100) NOT NULL,
  PRIMARY KEY (`investigator_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `department` varchar(100) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping events for database 'cyber_investigation'
--

--
-- Dumping routines for database 'cyber_investigation'
--
/*!50003 DROP FUNCTION IF EXISTS `CalculateIncidentAge` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `CalculateIncidentAge`(
    p_incident_id INT
) RETURNS int
    READS SQL DATA
BEGIN

    DECLARE v_reported_at DATETIME;

    SELECT reported_at
    INTO v_reported_at
    FROM Incidents
    WHERE incident_id = p_incident_id;

    IF v_reported_at IS NULL THEN
        RETURN NULL;
    END IF;

    RETURN DATEDIFF(CURDATE(), DATE(v_reported_at));

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `CalculateResolutionDuration` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `CalculateResolutionDuration`(
    p_incident_id INT
) RETURNS int
    READS SQL DATA
BEGIN

    DECLARE v_reported_at DATETIME;
    DECLARE v_resolved_at DATETIME;

    SELECT reported_at
    INTO v_reported_at
    FROM Incidents
    WHERE incident_id = p_incident_id;

    SELECT MIN(changed_at)
    INTO v_resolved_at
    FROM Incident_Status_History
    WHERE incident_id = p_incident_id
      AND new_status = 'Resolved';

    IF v_reported_at IS NULL OR v_resolved_at IS NULL THEN
        RETURN NULL;
    END IF;

    RETURN TIMESTAMPDIFF(
        HOUR,
        v_reported_at,
        v_resolved_at
    );

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AddIncident` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddIncident`(
    IN p_device_id INT,
    IN p_investigator_id INT,
    IN p_incident_type VARCHAR(100),
    IN p_description TEXT,
    IN p_severity VARCHAR(20),
    IN p_status VARCHAR(30)
)
BEGIN

    INSERT INTO Incidents
    (
        device_id,
        investigator_id,
        incident_type,
        description,
        severity,
        status,
        reported_at
    )
    VALUES
    (
        p_device_id,
        p_investigator_id,
        p_incident_type,
        p_description,
        p_severity,
        p_status,
        NOW()
    );

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AssignInvestigator` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AssignInvestigator`(
    IN p_incident_id INT,
    IN p_investigator_id INT
)
BEGIN

    UPDATE Incidents
    SET investigator_id = p_investigator_id
    WHERE incident_id = p_incident_id;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetIncidentDetails` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetIncidentDetails`(
    IN p_incident_id INT
)
BEGIN

    SELECT *
    FROM Incident_Report
    WHERE incident_id = p_incident_id;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `UpdateIncidentStatus` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateIncidentStatus`(
    IN p_incident_id INT,
    IN p_new_status VARCHAR(30)
)
BEGIN

    UPDATE Incidents
    SET status = p_new_status
    WHERE incident_id = p_incident_id;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Final view structure for view `Critical_Incident_Report`
--

/*!50001 DROP VIEW IF EXISTS `Critical_Incident_Report`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `Critical_Incident_Report` AS select `Incidents`.`incident_id` AS `incident_id`,`Incidents`.`incident_type` AS `incident_type`,`Incidents`.`severity` AS `severity`,`Incidents`.`status` AS `status`,`Incidents`.`reported_at` AS `reported_at` from `Incidents` where (`Incidents`.`severity` in ('High','Critical')) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `Incident_Report`
--

/*!50001 DROP VIEW IF EXISTS `Incident_Report`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `Incident_Report` AS select `i`.`incident_id` AS `incident_id`,`u`.`name` AS `affected_user`,`d`.`device_name` AS `device_name`,`d`.`device_type` AS `device_type`,`i`.`incident_type` AS `incident_type`,`i`.`description` AS `description`,`i`.`severity` AS `severity`,`i`.`status` AS `status`,`inv`.`name` AS `investigator`,`i`.`reported_at` AS `reported_at` from (((`Incidents` `i` join `Devices` `d` on((`i`.`device_id` = `d`.`device_id`))) join `Users` `u` on((`d`.`user_id` = `u`.`user_id`))) left join `Investigators` `inv` on((`i`.`investigator_id` = `inv`.`investigator_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `Investigator_Workload_Report`
--

/*!50001 DROP VIEW IF EXISTS `Investigator_Workload_Report`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `Investigator_Workload_Report` AS select `inv`.`investigator_id` AS `investigator_id`,`inv`.`name` AS `investigator_name`,`inv`.`role` AS `role`,count(`i`.`incident_id`) AS `total_incidents` from (`Investigators` `inv` left join `Incidents` `i` on((`inv`.`investigator_id` = `i`.`investigator_id`))) group by `inv`.`investigator_id`,`inv`.`name`,`inv`.`role` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-23  0:26:24

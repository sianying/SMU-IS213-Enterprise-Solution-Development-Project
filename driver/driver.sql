-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 19, 2021 at 03:32 PM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `driver`
--
CREATE DATABASE IF NOT EXISTS `driver` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `driver`;

-- --------------------------------------------------------

--
-- Table structure for table `driver`
--

DROP TABLE IF EXISTS `driver`;
CREATE TABLE IF NOT EXISTS `driver` (
  `driver_ID` int(2) NOT NULL AUTO_INCREMENT,
  `driver_name` varchar(64) NOT NULL,
  `driver_email` varchar(128) NOT NULL,
  `driver_mobile` int(8) NOT NULL,
  `driver_teleID` varchar(20) DEFAULT NULL,
  `vehicle_no` varchar(8) NOT NULL,
  `tele_chat_ID` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`driver_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `driver

INSERT INTO `driver` (`driver_ID`, `driver_name`, `driver_email`, `driver_mobile`, `driver_teleID`, `vehicle_no`, `tele_chat_ID`) VALUES
(6, 'Don', 'don@hotmail.com', 98765432, 'dontan', 'SJD1234A', "NULL"),
(7, 'Sandy', 'sandy@hotmail.com', 82345678, 'sandy', 'SJW1234F', "NULL"),
(8, 'Tom Smith', 'tomsmith@hotmail.com', 90293847, 'tommy', 'SBS1234A', "NULL"),
(9, 'Ubuntu', 'ubuntu@hotmail.com', 87246785, 'ubuntu', 'SBS5678A', "NULL"),
(10, 'yewteng', 'yewteng@hotmail.com', 90124289, 'YewTeng', 'SBS5678Y', 70827542);

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

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
-- Database: `customer`
--
CREATE DATABASE IF NOT EXISTS `customer` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `customer`;

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `customer_ID` int NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(64) NOT NULL,
  `customer_email` varchar(128) NOT NULL,
  `customer_mobile` int(8) NOT NULL,
  `customer_teleID` varchar(20) DEFAULT NULL,
  `tele_chat_ID` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`customer_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `customer

INSERT INTO `customer` (`customer_ID`, `customer_name`, `customer_email`, `customer_mobile`, `customer_teleID`, `tele_chat_ID`) VALUES
(9, 'jingwei', 'jingwei@gmail.com', 91231234, 'Jingweisim', 246939574),
(10, 'billy', 'billy@gmail.com', 82312312, 'billy', 'NULL'),
(13, 'kelly', 'kelly@gmail.com', 92312312, 'kelly', 'NULL'),
(15, 'helen', 'helen@gmail.com', 91435234, 'SianYing', 230470702),
(16, 'jwjw', 'jw@hotmail.com' , 94857362, 'jwjw', 'NULL');

-- (9, 'james', 'james@gmail.com', 91231234, 'james'),
-- (10, 'billy', 'billy@gmail.com', 12312312, 'billy'),
-- (13, 'kelly', 'kelly@gmail.com', 12312312, 'kelly'),
-- (15, 'helen', 'helen@gmail.com', 9123123, 'helen'),
-- (16, 'jwjw', 'jw@hotmail.com' ,91231234, 'jwjw');

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

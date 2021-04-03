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
SET time_zone = "+08:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `schedule`
--
CREATE DATABASE IF NOT EXISTS `schedule_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `schedule_db`;

-- --------------------------------------------------------

--
-- Table structure for table `schedule`
--

DROP TABLE IF EXISTS `schedule`;
CREATE TABLE IF NOT EXISTS `schedule` (
  `SID` int NOT NULL,
  `driver_ID` int NOT NULL,
  `delivery_date` date NOT NULL,
  `t_8_to_10` boolean not null,
  `t_10_to_12` boolean not null,
  `t_12_to_2` boolean not null,
  `t_2_to_4` boolean not null,
  `t_4_to_6` boolean not null,
  PRIMARY KEY (`SID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `order`
--

INSERT INTO `schedule` (`SID`, `driver_ID`, `delivery_date`, `t_8_to_10`, `t_10_to_12`, `t_12_to_2`, `t_2_to_4`, `t_4_to_6`) VALUES
(1, 23, '2020-06-12', 0 , 0, 0, 1, 0),
(2, 17, '2020-06-17', 0, 0, 0, 1, 1),
(3, 54, '2021-06-17', 0, 1, 0, 1, 1),
(4, 66, '2021-06-17', 1, 0, 0, 0, 1),
(5, 23, '2020-10-17', 0, 0, 1, 0, 0),
(6, 23, '2020-03-17', 1, 0, 1, 0, 1);

COMMIT;


select * from schedule;

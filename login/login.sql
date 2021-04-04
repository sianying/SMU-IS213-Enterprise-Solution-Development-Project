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
CREATE DATABASE IF NOT EXISTS `login` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `login`;

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `login`;
CREATE TABLE IF NOT EXISTS `login` (
  `username` varchar(64) NOT NULL,
  `password` varchar(12) NOT NULL,
  `account_type` varchar(8) NOT NULL,
  `ID` int NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `customer

INSERT INTO `login` (`username`, `password`, `account_type`, `ID`) VALUES
('jinglesim', 'password', 'customer', 0),
('sy', 'password123', 'customer', 1),
('tomsmith80', 'password', 'driver', '0');
-- ('Understanding People', '9781349471231', '99.40', 25),
-- ('Happy in Workplace', '9781434474234', '94.00', 1),
-- ('PHP Soup', '9781442374221', '20.50', 2),
-- ('Brief History of Time', '9781449474211', '20.00', 23),
-- ('It', '9781449474212', '1.00', 2),
-- ('Founder of Php', '9781449474221', '34.00', 1),
-- ('Albert Enstein\'s Works', '9781449474223', '18.00', 7),
-- ('Interstellar', '9781449474254', '10.00', 4),
-- ('Milk and Honey', '9781449474256', '25.00', 18),
-- ('Cooking Book', '9781449474323', '99.90', 4),
-- ('The Gathering', '9781449474342', '20.00', 50);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

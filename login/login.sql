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
    `customer_ID` int,
    `driver_ID` int,
    PRIMARY KEY (`username`),
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `customer

INSERT INTO `login` (`username`, `password`, `account_type`, `customer_ID`, `driver_ID`) VALUES
('jwjw', 'password', 'customer', 12345678, null),
('sysy', 'password123', 'customer', 23456789, null),
('liyin', 'liyin', 'customer', 11112222, null),
('SSLMonsta', 'security', 'driver', null, 17),
('tomsmith80', 'password', 'driver', null, 23),
('hongsengcurryrice', 'curryrice', 'driver', null, 54),
('yewteng', 'bestman', 'driver', null, 66);

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

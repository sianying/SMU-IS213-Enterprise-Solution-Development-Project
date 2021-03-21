
-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jun 12, 2020 at 02:17 AM
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
-- Database: `delivery`
--
CREATE DATABASE IF NOT EXISTS `delivery` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `delivery`;

-- --------------------------------------------------------

--
-- Table structure for table `delivery`
--


DROP TABLE IF EXISTS `delivery`;
CREATE TABLE IF NOT EXISTS `delivery` (
  `job_ID` int NOT NULL AUTO_INCREMENT,
  `driver_ID` int(2) NOT NULL,
  `customer_ID` int(8) NOT NULL,
  `delivery_date` date NOT NULL,
  `timeslot` varchar(20) NOT NULL,
  `pickup_location` varchar(60) NOT NULL,
  `destination` varchar(60) NOT NULL,
  `status` varchar(10) NOT NULL DEFAULT 'NEW',
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`job_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `order`
--

INSERT INTO `delivery` (`job_id`, `driver_ID`, `customer_ID`, `delivery_date`, `timeslot`, `pickup_location`, `destination`, `status`, `created`, `last_updated`) VALUES
(1, 23, 12345678 , '2020-06-12', '2_to_4', 'Lentor Ave Blk 25', 'Yishun Street 22 Blk 299', 'NEW', '2019-06-12 02:14:55', '2020-06-12 02:14:55');















-- --------------------------------------------------------

--
-- Table structure for table `order_item`
--

-- DROP TABLE IF EXISTS `order_item`;
-- CREATE TABLE IF NOT EXISTS `order_item` (
--   `item_id` int(11) NOT NULL AUTO_INCREMENT,
--   `order_id` int(11) NOT NULL,
--   `book_id` char(13) NOT NULL,
--   `quantity` int(11) NOT NULL,
--   PRIMARY KEY (`item_id`),
--   KEY `FK_order_id` (`order_id`)
-- ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- --
-- -- Dumping data for table `order_item`
-- --

-- INSERT INTO `order_item` (`item_id`, `order_id`, `book_id`, `quantity`) VALUES
-- (1, 1, '9781434474234', 1),
-- (2, 1, '9781449474212', 1);

-- --
-- -- Constraints for dumped tables
-- --

-- --
-- -- Constraints for table `order_item`
-- --
-- ALTER TABLE `order_item`
--   ADD CONSTRAINT `FK_order_id` FOREIGN KEY (`order_id`) REFERENCES `order` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE;
-- COMMIT;

-- /*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
-- /*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
-- /*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `cheetah_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `cheetah_db`;


DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
    `customer_ID` int NOT NULL AUTO_INCREMENT,
    `customer_name` varchar(64) NOT NULL,
    `customer_email` varchar(128) NOT NULL,
    `customer_mobile` int(8) NOT NULL,
    `customer_teleID` varchar(20) DEFAULT NULL,
    PRIMARY KEY (`customer_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `driver`;
CREATE TABLE IF NOT EXISTS `driver` (
  `driver_ID` int(2) NOT NULL AUTO_INCREMENT,
  `driver_name` varchar(64) NOT NULL,
  `driver_email` varchar(128) NOT NULL,
  `driver_mobile` int(8) NOT NULL,
  `driver_teleID` varchar(20) DEFAULT NULL,
  `vehicle_no` varchar(8) NOT NULL,
  PRIMARY KEY (`driver_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


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
    PRIMARY KEY (`SID`),
    FOREIGN KEY (`driver_ID`) REFERENCES driver(`driver_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `login`;
CREATE TABLE IF NOT EXISTS `login` (
    `username` varchar(64) NOT NULL,
    `password` varchar(12) NOT NULL,
    `account_type` varchar(8) NOT NULL,
    `customer_ID` int,
    `driver_ID` int,
    PRIMARY KEY (`username`),
    FOREIGN KEY (`customer_ID`) REFERENCES customer(`customer_ID`),
    FOREIGN KEY (`driver_ID`) REFERENCES driver(`driver_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `delivery`;
CREATE TABLE IF NOT EXISTS `delivery` (
    `delivery_ID` int NOT NULL AUTO_INCREMENT,
    `driver_ID` int NOT NULL,     
    `customer_ID` int NOT NULL,   
    `delivery_date` date NOT NULL,
    `timeslot` varchar(20) NOT NULL,
    `pickup_location` varchar(60) NOT NULL,
    `destination` varchar(60) NOT NULL,
    `delivery_item` varchar(40) NOT NULL,
    `description` varchar(120) NOT NULL,
    `payment_amount` int NOT NULL,
    `payment_status` varchar(6) NOT NULL,
    `receiver_name` varchar(64) NOT NULL,
    `delivery_status` varchar(10) NOT NULL DEFAULT 'NEW',
    `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`delivery_ID`),
    FOREIGN KEY (`driver_ID`) REFERENCES driver(`driver_ID`),
    FOREIGN KEY (`customer_ID`) REFERENCES customer(`customer_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



INSERT INTO `customer` (`customer_ID`, `customer_name`, `customer_email`, `customer_mobile`, `customer_teleID`) VALUES
(12345678, 'Jing Wei ', 'jingwei@hotmail.com', '91231234', NULL),
(23456789, 'Sian Ying', 'sygoh@hotmail.com', '81234567', 'sysy'),
(11112222, 'Li Yin', 'lly@hotmail.com', '91234567', 'lly');


INSERT INTO `driver` (`driver_ID`, `driver_name`, `driver_email`, `driver_mobile`, `driver_teleID`, `vehicle_no`) VALUES
(17, 'SSL Monster', 'sslmonster@hotmail.com', 12345678, 'SSLM', 'SJW1234F'),
(23, 'Tom Smith ', 'tomsmith@hotmail.com', 98765432, 'TS', 'SJD1234A'),
(54, 'Hong Seng', 'hs@hotmail.com', 10293847, 'nobluetooth', 'SBS1234A'),
(66, 'Yew Teng', 'yt@hotmail.com', 10000000, 'bestman', 'SBS5678A');


INSERT INTO `login` (`username`, `password`, `account_type`, `customer_ID`, `driver_ID`) VALUES
('jwjw', 'password', 'customer', 12345678, null),
('sysy', 'password123', 'customer', 23456789, null),
('liyin', 'liyin', 'customer', 11112222, null),
('SSLMonsta', 'security', 'driver', null, 17),
('tomsmith80', 'password', 'driver', null, 23),
('hongsengcurryrice', 'curryrice', 'driver', null, 54),
('yewteng', 'bestman', 'driver', null, 66);


INSERT INTO `schedule` (`SID`, `driver_ID`, `delivery_date`, `t_8_to_10`, `t_10_to_12`, `t_12_to_2`, `t_2_to_4`, `t_4_to_6`) VALUES
(1, 23, '2020-06-12', 0 , 0, 0, 1, 0),
(2, 17, '2020-06-17', 0, 0, 0, 1, 0),
(3, 54, '2021-06-17', 0, 1, 0, 1, 0),
(4, 66, '2021-06-17', 1, 0, 0, 0, 0),
(5, 23, '2020-10-17', 0, 0, 1, 0, 0),
(6, 23, '2020-03-17', 1, 0, 1, 0, 1);


INSERT INTO `delivery` (`delivery_ID`, `driver_ID`, `customer_ID`, `delivery_date`, `timeslot`, `pickup_location`, `destination`, `delivery_item`, `description`, `payment_amount`, `payment_status`, `receiver_name`, `delivery_status`,  `created`, `last_updated`) VALUES
(1, 23, 12345678, '2020-06-12', '2_to_4', 'Lentor Ave Blk 25', 'Yishun Street 22 Blk 299', 'Billy123', 'a cutie giraffe', '100', 'paid', 'sysy', 'On the way','2019-06-10 02:14:55', '2020-06-12 02:14:55'),
(2, 17, 23456789, '2020-06-17', '12_to_2', 'Bishan St 25 Blk 125', 'Tampines Street 17 Blk 300', 'uwubuntu', 'as cute as Billygoh', '100', 'paid', 'jwjw', 'On the way', '2019-06-15 03:14:55', '2020-06-17 02:14:55'),
(3, 54, 11112222, '2020-06-22', '2_to_4', 'Ang Mo Kio Street 34 Blk 277', 'Yishun Emerald Blk 23', 'apples', 'really fresh', '2000', 'unpaid', 'bernice', 'NEW', '2021-03-22 18:58:31', '2021-03-22 18:58:31'),
(4, 66, 12345678, '2021-04-01', '4_to_6', '81 Victoria St, Singapore 188065', '21 Lower Kent Ridge Rd, University Hall, Singapore 119077', 'knife', 'kidnap billy hehe', '3000', 'unpaid', 'zong', 'NEW', '2021-04-01 23:05:17', '2021-04-01 23:05:17');

COMMIT;


select * from delivery;
select * from customer;
select * from driver;
select * from schedule;
select * from login;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

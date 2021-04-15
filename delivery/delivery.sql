SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `delivery` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `delivery`;


DROP TABLE IF EXISTS `delivery`;
CREATE TABLE IF NOT EXISTS `delivery` (
    `delivery_ID` int NOT NULL AUTO_INCREMENT,
    `driver_ID` int NOT NULL,     
    `customer_ID` int(4) NOT NULL,   
    `delivery_date` date NOT NULL,
    `timeslot` varchar(20) NOT NULL,
    `pickup_location` varchar(60) NOT NULL,
    `destination` varchar(60) NOT NULL,
    `delivery_item` varchar(40) NOT NULL,
    `description` varchar(120) NOT NULL,
    `payment_amount` int NOT NULL,
    `payment_status` varchar(6) NOT NULL,
    `receiver_name` varchar(64) NOT NULL,
    `delivery_status` varchar(20) NOT NULL DEFAULT 'NEW',
    `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`delivery_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- INSERT INTO `delivery` (`delivery_ID`, `driver_ID`, `customer_ID`, `delivery_date`, `timeslot`, `pickup_location`, `destination`, `delivery_item`, `description`, `payment_amount`, `payment_status`, `receiver_name`, `delivery_status`,  `created`, `last_updated`) VALUES
-- (1, 2, 1001, '2021-04-12', '2_to_4', '930 Yishun Ave 2, Singapore 769098', '9 Bishan Pl, Singapore 579837', 'Billy123', 'a cutie giraffe', '100', 'paid', 'sysy', 'Completed!','2021-03-10 02:14:55', '2021-04-12 16:00:00'),
-- (2, 1, 1002, '2021-04-17', '2_to_4', '4 Tampines Central 5, Singapore 529510', '1 Woodlands Square, Singapore 738099', 'uwubuntu', 'as cute as Billygoh', '100', 'paid', 'jwjw', 'In Progress', '2021-04-10 11:14:55', '2021-04-17 13:14:55'),
-- (3, 2, 1003, '2021-04-17', '8_to_10', '2 Handy Road, Singapore 229233', '1 Jurong West Central 2, Singapore 648886', 'pullup bar', 'wanna get ripped', '2500', 'paid', 'jwjw', 'In Progress', '2021-04-10 11:14:55', '2021-04-17 13:14:55'),
-- (4, 2, 1004, '2021-04-17', '2_to_4', '2 Jurong East Street 21, Singapore 609601', '50 Jurong Gateway Rd, Singapore 608549', 'pullup bar', 'wanna get ripped', '2500', 'paid', 'jwjw', 'In Progress', '2021-04-10 11:14:55', '2021-04-17 13:14:55'),
-- (5, 3, 1001, '2021-04-17', '8_to_10', '1 Raffles Link, Singapore 039393', '2 Tampines Central 5, #01-32 Century Square, Singapore 529509', 'pullup bar', 'wanna get ripped', '2500', 'paid', 'sysy', 'In Progress', '2021-04-10 11:14:55', '2021-04-17 13:14:55'),
-- (6, 3, 1003, '2021-04-22', '2_to_4', '53 Ang Mo Kio Ave 3, Singapore 569933', '2 Orchard Turn, ION Orchard, 238801', 'apples', 'really fresh', '2000', 'unpaid', 'bernice', 'NEW', '2021-04-15 18:58:31', '2021-04-15 18:58:31'),
-- (7, 4, 1001, '2021-04-25', '4_to_6', '81 Victoria St, Singapore 188065', '21 Lower Kent Ridge Rd, University Hall, Singapore 119077', 'knife', 'kidnap billy hehe', '3000', 'unpaid', 'zong', 'NEW', '2021-04-16 23:05:17', '2021-04-16 23:05:17'),
-- (8, 2, 1004, '2021-04-25', '10_to_12', '81 Victoria St, Singapore 188065', '21 Lower Kent Ridge Rd, University Hall, Singapore 119077', 'knife', 'kidnap billy hehe', '3000', 'unpaid', 'zong', 'NEW', '2021-04-16 23:05:17', '2021-04-16 23:05:17');

-- COMMIT;


select * from delivery;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
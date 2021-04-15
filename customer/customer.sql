SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `customer` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `customer`;


DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
    `customer_ID` int(4) NOT NULL AUTO_INCREMENT,
    `customer_name` varchar(64) NOT NULL,
    `customer_email` varchar(128) NOT NULL,
    `customer_mobile` int(8) NOT NULL,
    `customer_teleID` varchar(20) DEFAULT NULL,
    `tele_chat_ID` varchar(15) DEFAULT NULL,
    PRIMARY KEY (`customer_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- INSERT INTO `customer` (`customer_ID`, `customer_name`, `customer_email`, `customer_mobile`, `customer_teleID`, `tele_chat_ID`) VALUES
-- (1001, 'Jing Wei ', 'jw@hotmail.com', 98723645, 'Jingweisim', '246939574'),
-- (1002, 'bernice', 'ber@gmail.com', 90387648, 'Namisus', '828731935');


-- COMMIT;

select * from customer;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

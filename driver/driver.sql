SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `driver` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `driver`;


DROP TABLE IF EXISTS `driver`;
CREATE TABLE IF NOT EXISTS `driver` (
  `driver_ID` int NOT NULL AUTO_INCREMENT,
  `driver_name` varchar(64) NOT NULL,
  `driver_email` varchar(128) NOT NULL,
  `driver_mobile` int(8) NOT NULL,
  `driver_teleID` varchar(20) DEFAULT NULL,
  `tele_chat_ID` varchar(15) DEFAULT NULL,
  `vehicle_no` varchar(8) NOT NULL,
  PRIMARY KEY (`driver_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- INSERT INTO `driver` (`driver_ID`, `driver_name`, `driver_email`, `driver_mobile`, `driver_teleID`, `tele_chat_ID`, `vehicle_no`) VALUES
-- (1, 'Zong Han', 'zh@gmail.com', 90458475, 'zongee', '735505752', 'SGD1233Z'),
-- (2, 'sian ying ', 'sy@gmail.com', 90123243, 'SianYing', '230470702', 'SJD1234A'),
-- (3, 'Li Yin', 'liyin@gmail.com', 98712372, 'liyin00', '519142989', 'SBS1234A');


-- COMMIT;


select * from driver;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3307
-- Generation Time: Mar 01, 2026 at 09:53 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `internship_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `employee_contact`
--

CREATE TABLE `employee_contact` (
  `id` int(11) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `employee_finance`
--

CREATE TABLE `employee_finance` (
  `id` int(11) NOT NULL,
  `salary` decimal(10,2) DEFAULT NULL,
  `pan_card` varchar(20) DEFAULT NULL,
  `bank_name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `employee_identity`
--

CREATE TABLE `employee_identity` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `employee_personal`
--

CREATE TABLE `employee_personal` (
  `id` int(11) NOT NULL,
  `dob` date DEFAULT NULL,
  `blood_group` varchar(5) DEFAULT NULL,
  `emergency_contact` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `employee_table`
--

CREATE TABLE `employee_table` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `emp_detail`
--

CREATE TABLE `emp_detail` (
  `id` int(11) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `dob` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `employee_contact`
--
ALTER TABLE `employee_contact`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `employee_finance`
--
ALTER TABLE `employee_finance`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `employee_identity`
--
ALTER TABLE `employee_identity`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `employee_personal`
--
ALTER TABLE `employee_personal`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `employee_table`
--
ALTER TABLE `employee_table`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `emp_detail`
--
ALTER TABLE `emp_detail`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `employee_contact`
--
ALTER TABLE `employee_contact`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `employee_finance`
--
ALTER TABLE `employee_finance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `employee_identity`
--
ALTER TABLE `employee_identity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `employee_personal`
--
ALTER TABLE `employee_personal`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `employee_table`
--
ALTER TABLE `employee_table`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `emp_detail`
--
ALTER TABLE `emp_detail`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

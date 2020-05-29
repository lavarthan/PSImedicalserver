-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 20, 2020 at 08:37 AM
-- Server version: 10.1.38-MariaDB
-- PHP Version: 7.3.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `medical_services`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointment_details`
--

CREATE TABLE `appointment_details` (
  `id` int(10) NOT NULL,
  `name` text NOT NULL,
  `date` varchar(100) NOT NULL,
  `time` varchar(100) NOT NULL,
  `hospital` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf32;

--
-- Dumping data for table `appointment_details`
--

INSERT INTO `appointment_details` (`id`, `name`, `date`, `time`, `hospital`) VALUES
(1, 'Mohan', '05/04/2020', '10 AM - 10.30 AM', 'Jaffna Teaching Hospital'),
(2, 'Mohan', '05/04/2020', '10.30 AM - 11.00 AM', 'Jaffna Teaching Hospital');

-- --------------------------------------------------------

--
-- Table structure for table `complain_details`
--

CREATE TABLE `complain_details` (
  `id` int(10) NOT NULL,
  `name` varchar(100) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `complain` varchar(2500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf32;

--
-- Dumping data for table `complain_details`
--

INSERT INTO `complain_details` (`id`, `name`, `date`, `complain`) VALUES
(4, 'user_name', '0000-00-00 00:00:00', 'today i faced a really bad service in jaffna teaching hospital'),
(5, 'user_name', '0000-00-00 00:00:00', 'today i faced a really bad service in jaffna teaching hospital'),
(6, 'user_name', '0000-00-00 00:00:00', 'today i faced a really bad service in jaffna teaching hospital'),
(7, 'user_name', '0000-00-00 00:00:00', 'today i faced a really bad service in jaffna teaching hospital'),
(8, 'nisanthan', '2020-04-30 02:45:05', 'Jaffna teaching hopital is not opening on time.'),
(9, 'user_name', '2020-04-30 04:02:00', 'i faced big issue'),
(10, 'user_name', '2020-05-20 03:34:46', 'ok');

-- --------------------------------------------------------

--
-- Table structure for table `doctor_details`
--

CREATE TABLE `doctor_details` (
  `id` int(100) NOT NULL,
  `name` text NOT NULL,
  `working_hospitals` varchar(255) NOT NULL,
  `about` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf32;

--
-- Dumping data for table `doctor_details`
--

INSERT INTO `doctor_details` (`id`, `name`, `working_hospitals`, `about`) VALUES
(1, 'Mohan', 'Jaffna Teaching Hospital', 'Dr.Mohan is an eye surgeon.');

-- --------------------------------------------------------

--
-- Table structure for table `hospital_details`
--

CREATE TABLE `hospital_details` (
  `id` int(100) NOT NULL,
  `name` text NOT NULL,
  `location` varchar(255) NOT NULL,
  `services` varchar(2550) NOT NULL,
  `district` varchar(2550) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf32;

--
-- Dumping data for table `hospital_details`
--

INSERT INTO `hospital_details` (`id`, `name`, `location`, `services`, `district`) VALUES
(1, 'Jaffna Teaching Hospital', 'Hospital St, Jaffna 40000', 'cardiology, diabetic, dentistry, dermatology, family planning, gynecology, neurology, obstetrics (ante-natal), oncology, ophthalmology, orthopedics, otolaryngology (ENT), pediatrics and psychiatry', 'Jaffna');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointment_details`
--
ALTER TABLE `appointment_details`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `complain_details`
--
ALTER TABLE `complain_details`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `doctor_details`
--
ALTER TABLE `doctor_details`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `hospital_details`
--
ALTER TABLE `hospital_details`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appointment_details`
--
ALTER TABLE `appointment_details`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `complain_details`
--
ALTER TABLE `complain_details`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `doctor_details`
--
ALTER TABLE `doctor_details`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `hospital_details`
--
ALTER TABLE `hospital_details`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

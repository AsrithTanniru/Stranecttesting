-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 29, 2023 at 12:49 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `apihub`
--

-- --------------------------------------------------------

--
-- Table structure for table `stats`
--

CREATE TABLE `stats` (
  `id` int(50) NOT NULL,
  `sid` varchar(90) NOT NULL,
  `profile` int(11) NOT NULL,
  `interests` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `stats`
--

INSERT INTO `stats` (`id`, `sid`, `profile`, `interests`) VALUES
(4, 'Wa6YDKIqlJXoMu8ZyFAQX0uCKyEyA9Klv60', 0, 1),
(5, 'UuHjYqu91YKKjf3OJ5M4ox4AmiEx4g', 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `tokens`
--

CREATE TABLE `tokens` (
  `tokenid` int(50) NOT NULL,
  `id` int(50) NOT NULL,
  `username` varchar(40) NOT NULL,
  `token` varchar(600) NOT NULL,
  `valid` tinyint(1) NOT NULL,
  `aid` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tokens`
--

INSERT INTO `tokens` (`tokenid`, `id`, `username`, `token`, `valid`, `aid`) VALUES
(47, 99, 'kousic', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImtvdXNpYyIsImlwIjoiMTI3LjAuMC4xIiwiZXhwIjoxNjkzMzkxNjY4LCJ1c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExNi4wLjAuMCBTYWZhcmkvNTM3LjM2Iiwic2lkIjoiV2E2WURLSXFsSlhvTXU4WnlGQVFYMHVDS3lFeUE5S2x2NjAifQ.EUgqzcyfP7noAC5ZmvM9uJ9NaEPv-xo3jwNJlpxyj4s', 1, '1rjBP92uzr9Q0aGFOblODonid3vbO8a618zaS1f4lm0K30hwFk');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(500) NOT NULL,
  `password` varchar(500) NOT NULL,
  `aid` varchar(100) NOT NULL,
  `sid` varchar(100) NOT NULL,
  `datetime` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `aid`, `sid`, `datetime`) VALUES
(99, 'kousic', '$argon2id$v=19$m=65536,t=3,p=4$Ge0YRJ+9Kx232qDcAgHxFA$tEfxcD8SLf+Ee+W0WVCP/Wjx5TkoU507ZmT6kRl7ZkE', '1rjBP92uzr9Q0aGFOblODonid3vbO8a618zaS1f4lm0K30hwFk', 'Wa6YDKIqlJXoMu8ZyFAQX0uCKyEyA9Klv60', 'Aug 29 2023 04:04PM');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `stats`
--
ALTER TABLE `stats`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sid` (`sid`);

--
-- Indexes for table `tokens`
--
ALTER TABLE `tokens`
  ADD PRIMARY KEY (`tokenid`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`,`datetime`),
  ADD KEY `username` (`username`),
  ADD KEY `aid` (`aid`),
  ADD KEY `sid` (`sid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `stats`
--
ALTER TABLE `stats`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `tokens`
--
ALTER TABLE `tokens`
  MODIFY `tokenid` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

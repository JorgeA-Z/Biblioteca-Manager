-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 20-05-2022 a las 19:12:00
-- Versión del servidor: 10.4.24-MariaDB
-- Versión de PHP: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `biblioteca`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cobro`
--

CREATE TABLE `cobro` (
  `IDCOBRO` int(11) NOT NULL,
  `IDPRESTAMO` int(11) NOT NULL,
  `ESTADO` tinyint(1) DEFAULT 0,
  `ENTREGA` date NOT NULL,
  `ENTREGAREAL` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detallecobro`
--

CREATE TABLE `detallecobro` (
  `IDDETALLECOBRO` int(11) NOT NULL,
  `IDCOBRO` int(11) NOT NULL,
  `IDLIBRO` int(11) NOT NULL,
  `DAMAGE` varchar(9) NOT NULL,
  `MONTO` float NOT NULL,
  `ESTADO` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalleprestamo`
--

CREATE TABLE `detalleprestamo` (
  `IDDETALEPRESTAMO` int(11) NOT NULL,
  `IDPRESTAMO` int(11) NOT NULL,
  `IDLIBRO` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado`
--

CREATE TABLE `empleado` (
  `RFC` varchar(13) NOT NULL,
  `CONTRASEÑA` varchar(16) NOT NULL,
  `NOMBRE` varchar(100) NOT NULL,
  `INGRESO` timestamp NOT NULL DEFAULT current_timestamp(),
  `TELEFONO` bigint(10) NOT NULL,
  `SALARIO` double NOT NULL,
  `CARGO` varchar(13) NOT NULL,
  `DOMICILIO` varchar(100) NOT NULL,
  `ESTADO` tinyint(1) DEFAULT 1,
  `CORREO` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `libro`
--

CREATE TABLE `libro` (
  `IDLIBRO` int(11) NOT NULL,
  `IDTITULO` varchar(13) NOT NULL,
  `EJEMPLAR` int(11) NOT NULL,
  `COSTO` float NOT NULL,
  `DAÑOS` varchar(9) NOT NULL,
  `ESTADO` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `membresia`
--

CREATE TABLE `membresia` (
  `IDMEMBRESIA` int(11) NOT NULL,
  `IDUSUARIO` int(11) NOT NULL,
  `NACIMIENTO` date NOT NULL,
  `DOMICILIO` varchar(100) NOT NULL,
  `EXPIRACION` date NOT NULL,
  `EXPEDICION` timestamp NOT NULL DEFAULT current_timestamp(),
  `CORREO` varchar(100) NOT NULL,
  `ESTADO` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prestamo`
--

CREATE TABLE `prestamo` (
  `IDPRESTAMO` int(11) NOT NULL,
  `IDMEMBRESIA` int(11) NOT NULL,
  `SOLICITUD` timestamp NOT NULL DEFAULT current_timestamp(),
  `ENTREGA` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `titulo`
--

CREATE TABLE `titulo` (
  `IDTITULO` varchar(13) NOT NULL,
  `NOMBRE` varchar(100) NOT NULL,
  `AUTOR` varchar(100) NOT NULL,
  `EDICION` int(11) NOT NULL,
  `SCDD` bigint(10) NOT NULL,
  `EDITORIAL` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `IDUSUARIO` int(11) NOT NULL,
  `NOMBRE` varchar(100) NOT NULL,
  `CONTRASEÑA` varchar(16) NOT NULL,
  `TELEFONO` bigint(10) NOT NULL,
  `ESTADO` tinyint(1) DEFAULT 1,
  `TIPO` varchar(13) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `visitas`
--

CREATE TABLE `visitas` (
  `IDVISITA` int(11) NOT NULL,
  `IDUSUARIO` int(11) NOT NULL,
  `VISITA` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cobro`
--
ALTER TABLE `cobro`
  ADD PRIMARY KEY (`IDCOBRO`),
  ADD KEY `IDPRESTAMO` (`IDPRESTAMO`);

--
-- Indices de la tabla `detallecobro`
--
ALTER TABLE `detallecobro`
  ADD PRIMARY KEY (`IDDETALLECOBRO`),
  ADD KEY `IDCOBRO` (`IDCOBRO`),
  ADD KEY `IDLIBRO` (`IDLIBRO`);

--
-- Indices de la tabla `detalleprestamo`
--
ALTER TABLE `detalleprestamo`
  ADD PRIMARY KEY (`IDDETALEPRESTAMO`),
  ADD KEY `IDPRESTAMO` (`IDPRESTAMO`),
  ADD KEY `IDLIBRO` (`IDLIBRO`);

--
-- Indices de la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD PRIMARY KEY (`RFC`);

--
-- Indices de la tabla `libro`
--
ALTER TABLE `libro`
  ADD PRIMARY KEY (`IDLIBRO`),
  ADD KEY `libro_ibfk_1` (`IDTITULO`);

--
-- Indices de la tabla `membresia`
--
ALTER TABLE `membresia`
  ADD PRIMARY KEY (`IDMEMBRESIA`),
  ADD KEY `IDUSUARIO` (`IDUSUARIO`);

--
-- Indices de la tabla `prestamo`
--
ALTER TABLE `prestamo`
  ADD PRIMARY KEY (`IDPRESTAMO`),
  ADD KEY `IDMEMBRESIA` (`IDMEMBRESIA`);

--
-- Indices de la tabla `titulo`
--
ALTER TABLE `titulo`
  ADD PRIMARY KEY (`IDTITULO`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`IDUSUARIO`);

--
-- Indices de la tabla `visitas`
--
ALTER TABLE `visitas`
  ADD PRIMARY KEY (`IDVISITA`),
  ADD KEY `IDUSUARIO` (`IDUSUARIO`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cobro`
--
ALTER TABLE `cobro`
  MODIFY `IDCOBRO` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detallecobro`
--
ALTER TABLE `detallecobro`
  MODIFY `IDDETALLECOBRO` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detalleprestamo`
--
ALTER TABLE `detalleprestamo`
  MODIFY `IDDETALEPRESTAMO` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `libro`
--
ALTER TABLE `libro`
  MODIFY `IDLIBRO` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `membresia`
--
ALTER TABLE `membresia`
  MODIFY `IDMEMBRESIA` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `prestamo`
--
ALTER TABLE `prestamo`
  MODIFY `IDPRESTAMO` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `IDUSUARIO` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `visitas`
--
ALTER TABLE `visitas`
  MODIFY `IDVISITA` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `cobro`
--
ALTER TABLE `cobro`
  ADD CONSTRAINT `cobro_ibfk_1` FOREIGN KEY (`IDPRESTAMO`) REFERENCES `prestamo` (`IDPRESTAMO`);

--
-- Filtros para la tabla `detallecobro`
--
ALTER TABLE `detallecobro`
  ADD CONSTRAINT `detallecobro_ibfk_1` FOREIGN KEY (`IDCOBRO`) REFERENCES `cobro` (`IDCOBRO`),
  ADD CONSTRAINT `detallecobro_ibfk_2` FOREIGN KEY (`IDLIBRO`) REFERENCES `libro` (`IDLIBRO`);

--
-- Filtros para la tabla `detalleprestamo`
--
ALTER TABLE `detalleprestamo`
  ADD CONSTRAINT `detalleprestamo_ibfk_1` FOREIGN KEY (`IDPRESTAMO`) REFERENCES `prestamo` (`IDPRESTAMO`),
  ADD CONSTRAINT `detalleprestamo_ibfk_2` FOREIGN KEY (`IDLIBRO`) REFERENCES `libro` (`IDLIBRO`);

--
-- Filtros para la tabla `libro`
--
ALTER TABLE `libro`
  ADD CONSTRAINT `libro_ibfk_1` FOREIGN KEY (`IDTITULO`) REFERENCES `titulo` (`IDTITULO`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `membresia`
--
ALTER TABLE `membresia`
  ADD CONSTRAINT `membresia_ibfk_1` FOREIGN KEY (`IDUSUARIO`) REFERENCES `usuario` (`IDUSUARIO`);

--
-- Filtros para la tabla `prestamo`
--
ALTER TABLE `prestamo`
  ADD CONSTRAINT `prestamo_ibfk_1` FOREIGN KEY (`IDMEMBRESIA`) REFERENCES `membresia` (`IDMEMBRESIA`);

--
-- Filtros para la tabla `visitas`
--
ALTER TABLE `visitas`
  ADD CONSTRAINT `visitas_ibfk_1` FOREIGN KEY (`IDUSUARIO`) REFERENCES `usuario` (`IDUSUARIO`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

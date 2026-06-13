-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: db_sxf
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `consulta`
--

DROP TABLE IF EXISTS `consulta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consulta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idPaciente` int(11) NOT NULL,
  `idPesquisador` int(11) NOT NULL,
  `dataHora` datetime NOT NULL,
  `tipoExame` varchar(100) NOT NULL,
  `resultadoExame` varchar(50) NOT NULL,
  `pontuacao` decimal(4,2) NOT NULL,
  `encaminhamento` varchar(100) NOT NULL,
  `observacao` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idPaciente` (`idPaciente`),
  KEY `idPesquisador` (`idPesquisador`),
  CONSTRAINT `consulta_ibfk_1` FOREIGN KEY (`idPaciente`) REFERENCES `paciente` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `consulta_ibfk_2` FOREIGN KEY (`idPesquisador`) REFERENCES `usuario` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consulta`
--

LOCK TABLES `consulta` WRITE;
/*!40000 ALTER TABLE `consulta` DISABLE KEYS */;
INSERT INTO `consulta` VALUES (1,1,1,'2026-05-01 09:15:00','Triagem Inicial','Positivo',0.78,'Fazer teste','Apresenta múltiplos sinais compatíveis.'),(2,2,1,'2026-05-01 10:30:00','Triagem Inicial','Negativo',0.11,'Diagnóstico limpo','Poucos sintomas observados.'),(3,3,1,'2026-05-02 08:45:00','Avaliação Clínica','Positivo',0.63,'Fazer teste','Necessita investigação complementar.'),(4,4,1,'2026-05-02 14:20:00','Avaliação Clínica','Negativo',0.09,'Diagnóstico limpo','Sem indícios relevantes.'),(5,5,1,'2026-05-03 11:00:00','Triagem Inicial','Positivo',0.54,'Fazer teste','Sintomas moderados observados.'),(6,6,1,'2026-05-03 15:40:00','Avaliação Clínica','Negativo',0.15,'Diagnóstico limpo','Acompanhamento recomendado.'),(7,7,1,'2026-05-04 09:10:00','Triagem Inicial','Positivo',0.72,'Fazer teste','Pontuação elevada.'),(8,1,1,'2026-05-05 10:00:00','Reavaliação','Positivo',0.81,'Fazer teste','Persistência dos sintomas.'),(9,2,1,'2026-05-05 13:50:00','Reavaliação','Negativo',0.18,'Diagnóstico limpo','Melhora observada.'),(10,3,1,'2026-05-06 08:20:00','Triagem Inicial','Positivo',0.59,'Fazer teste','Necessita nova avaliação.'),(11,4,1,'2026-05-06 14:10:00','Triagem Inicial','Negativo',0.05,'Diagnóstico limpo','Nenhum sintoma relevante.'),(12,5,1,'2026-05-07 09:30:00','Avaliação Clínica','Positivo',0.67,'Fazer teste','Diversos sintomas identificados.'),(13,6,1,'2026-05-07 15:00:00','Triagem Inicial','Negativo',0.14,'Diagnóstico limpo','Baixa incidência de sintomas.'),(14,7,1,'2026-05-08 11:15:00','Avaliação Clínica','Positivo',0.76,'Fazer teste','Indícios fortes para investigação.'),(15,1,1,'2026-05-09 10:40:00','Avaliação Clínica','Positivo',0.70,'Fazer teste','Quadro consistente.'),(16,2,1,'2026-05-09 16:20:00','Triagem Inicial','Negativo',0.08,'Diagnóstico limpo','Sem alterações significativas.'),(17,3,1,'2026-05-10 08:55:00','Reavaliação','Positivo',0.65,'Fazer teste','Mantém sinais observados anteriormente.'),(18,4,1,'2026-05-10 13:25:00','Reavaliação','Negativo',0.12,'Diagnóstico limpo','Resultado dentro do esperado.'),(19,5,1,'2026-05-11 09:45:00','Triagem Inicial','Positivo',0.57,'Fazer teste','Sintomas moderados persistem.'),(20,7,1,'2026-05-11 15:30:00','Reavaliação','Positivo',0.74,'Fazer teste','Necessita encaminhamento especializado.'),(21,8,1,'2026-05-12 09:00:00','Triagem Inicial','Positivo',0.61,'Fazer teste','Indícios moderados.'),(22,9,1,'2026-05-12 10:15:00','Triagem Inicial','Negativo',0.09,'Diagnóstico limpo','Sem alterações relevantes.'),(23,10,1,'2026-05-12 14:30:00','Avaliação Clínica','Positivo',0.72,'Fazer teste','Sintomas relevantes.'),(24,11,1,'2026-05-13 08:45:00','Reavaliação','Positivo',0.66,'Fazer teste','Persistência dos sintomas.'),(25,12,1,'2026-05-13 10:20:00','Triagem Inicial','Negativo',0.13,'Diagnóstico limpo','Baixa incidência.'),(26,13,1,'2026-05-13 15:40:00','Avaliação Clínica','Positivo',0.79,'Fazer teste','Pontuação elevada.'),(27,14,1,'2026-05-14 09:30:00','Triagem Inicial','Negativo',0.11,'Diagnóstico limpo','Sem indícios importantes.'),(28,15,1,'2026-05-14 13:50:00','Reavaliação','Positivo',0.69,'Fazer teste','Necessita acompanhamento.'),(29,8,1,'2025-04-05 09:15:00','Triagem Inicial','Positivo',0.74,'Fazer teste','Histórico anterior.'),(30,9,1,'2025-06-10 10:00:00','Triagem Inicial','Negativo',0.10,'Diagnóstico limpo','Sem sintomas relevantes.'),(31,10,1,'2025-08-12 14:10:00','Avaliação Clínica','Positivo',0.63,'Fazer teste','Necessita acompanhamento.'),(32,11,1,'2025-09-01 16:00:00','Triagem Inicial','Positivo',0.71,'Fazer teste','Pontuação elevada.'),(33,12,1,'2024-03-15 08:20:00','Reavaliação','Negativo',0.08,'Diagnóstico limpo','Histórico antigo.'),(34,13,1,'2024-05-10 13:45:00','Triagem Inicial','Positivo',0.76,'Fazer teste','Diversos sintomas observados.'),(35,14,1,'2024-08-18 15:30:00','Avaliação Clínica','Negativo',0.12,'Diagnóstico limpo','Poucos indícios.'),(36,15,1,'2024-10-02 11:15:00','Triagem Inicial','Positivo',0.68,'Fazer teste','Necessita investigação.'),(37,1,1,'2026-05-15 09:00:00','Reavaliação','Positivo',0.82,'Fazer teste','Aumento da pontuação.'),(38,3,1,'2026-05-15 11:20:00','Triagem Inicial','Positivo',0.58,'Fazer teste','Sintomas moderados.'),(39,5,1,'2026-05-16 10:40:00','Avaliação Clínica','Positivo',0.73,'Fazer teste','Persistência observada.'),(40,7,1,'2026-05-16 15:10:00','Reavaliação','Positivo',0.77,'Fazer teste','Necessita encaminhamento.');
/*!40000 ALTER TABLE `consulta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consultasintoma`
--

DROP TABLE IF EXISTS `consultasintoma`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consultasintoma` (
  `idConsulta` int(11) NOT NULL,
  `idSintoma` int(11) NOT NULL,
  PRIMARY KEY (`idConsulta`,`idSintoma`),
  KEY `idSintoma` (`idSintoma`),
  CONSTRAINT `consultasintoma_ibfk_1` FOREIGN KEY (`idConsulta`) REFERENCES `consulta` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `consultasintoma_ibfk_2` FOREIGN KEY (`idSintoma`) REFERENCES `sintoma` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consultasintoma`
--

LOCK TABLES `consultasintoma` WRITE;
/*!40000 ALTER TABLE `consultasintoma` DISABLE KEYS */;
INSERT INTO `consultasintoma` VALUES (1,1),(1,2),(1,5),(2,10),(2,11),(3,1),(3,6),(3,8),(4,10),(4,12),(5,5),(5,6),(5,9),(5,10),(6,9),(6,10),(7,1),(7,2),(7,4),(8,1),(8,2),(8,5),(8,6),(9,5),(10,1),(10,8),(10,9),(11,11),(12,1),(12,5),(12,10),(13,6),(14,1),(14,2),(14,6),(15,1),(15,5),(15,8),(15,10),(16,10),(17,1),(17,5),(17,6),(18,9),(19,5),(19,6),(19,8),(20,1),(20,2),(20,5),(21,1),(21,5),(21,6),(22,10),(23,1),(23,2),(23,5),(24,1),(24,6),(24,8),(25,11),(25,12),(26,1),(26,2),(26,5),(26,6),(27,10),(27,11),(28,1),(28,5),(28,8),(29,1),(29,2),(29,5),(29,6),(30,10),(31,1),(31,5),(31,8),(32,1),(32,2),(32,6),(33,11),(34,1),(34,2),(34,5),(34,8),(35,10),(35,12),(36,1),(36,5),(36,6),(37,1),(37,2),(37,5),(37,6),(38,5),(38,6),(38,8),(39,1),(39,2),(39,5),(40,1),(40,2),(40,5),(40,8);
/*!40000 ALTER TABLE `consultasintoma` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paciente`
--

DROP TABLE IF EXISTS `paciente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `paciente` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idCriador` int(11) NOT NULL,
  `idPesquisador` int(11) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `cpf` char(11) NOT NULL,
  `sexo` enum('Masculino','Feminino') NOT NULL,
  `dataNascimento` date NOT NULL,
  `ultimoTeste` datetime DEFAULT NULL,
  `dataCriacao` datetime NOT NULL DEFAULT current_timestamp(),
  `fotoPerfil` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idCriador` (`idCriador`),
  KEY `idPesquisador` (`idPesquisador`),
  CONSTRAINT `paciente_ibfk_1` FOREIGN KEY (`idCriador`) REFERENCES `usuario` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `paciente_ibfk_2` FOREIGN KEY (`idPesquisador`) REFERENCES `usuario` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paciente`
--

LOCK TABLES `paciente` WRITE;
/*!40000 ALTER TABLE `paciente` DISABLE KEYS */;
INSERT INTO `paciente` VALUES (1,1,2,'Lucas Alves de Lima','19201843911','Masculino','2007-07-25','2025-08-18 00:00:00','2026-06-12 10:57:57',NULL),(2,1,2,'Maria Santos da Aparecida','98191232932','Feminino','2005-04-12','2023-04-22 00:00:00','2026-06-12 10:57:57',NULL),(3,1,2,'João Nunes Claro','54150903923','Masculino','1999-02-28','2022-12-10 00:00:00','2026-06-12 10:57:57',NULL),(4,1,2,'Clara Tomas Domm','26606992469','Feminino','2010-10-20','2020-07-04 00:00:00','2026-06-12 10:57:57',NULL),(5,1,2,'Tomas Junior','99035339964','Masculino','2012-03-24','2026-02-20 00:00:00','2026-06-12 10:57:57',NULL),(6,1,2,'Fernando Luiz Lima','94965635123','Masculino','1981-06-20','2025-03-31 00:00:00','2026-06-12 10:57:57',NULL),(7,1,2,'Luiza das Flores','21674626064','Feminino','1975-07-10','2024-10-25 00:00:00','2026-06-12 10:57:57',NULL),(8,1,2,'Ana Carolina Souza','41786291011','Feminino','1998-03-15','2026-04-10 00:00:00','2026-06-12 10:57:57',NULL),(9,1,2,'Pedro Henrique Silva','51094732018','Masculino','2001-09-22','2026-03-28 00:00:00','2026-06-12 10:57:57',NULL),(10,1,2,'Juliana Mendes Rocha','89321764020','Feminino','2011-11-05','2026-05-15 00:00:00','2026-06-12 10:57:57',NULL),(11,1,2,'Carlos Eduardo Ramos','72819435055','Masculino','1988-01-12','2026-02-18 00:00:00','2026-06-12 10:57:57',NULL),(12,1,2,'Fernanda Oliveira','61038572099','Feminino','1995-06-30','2026-01-21 00:00:00','2026-06-12 10:57:57',NULL),(13,1,2,'Ricardo Gomes','18932745066','Masculino','1979-08-09','2026-05-01 00:00:00','2026-06-12 10:57:57',NULL),(14,1,2,'Patricia Costa','34871269034','Feminino','2008-12-17','2026-04-22 00:00:00','2026-06-12 10:57:57',NULL),(15,1,2,'Gabriel Martins','29047183072','Masculino','2013-02-03','2026-05-08 00:00:00','2026-06-12 10:57:57',NULL);
/*!40000 ALTER TABLE `paciente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sintoma`
--

DROP TABLE IF EXISTS `sintoma`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sintoma` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `pesoMasculino` decimal(4,2) NOT NULL,
  `pesoFeminino` decimal(4,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nome` (`nome`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sintoma`
--

LOCK TABLES `sintoma` WRITE;
/*!40000 ALTER TABLE `sintoma` DISABLE KEYS */;
INSERT INTO `sintoma` VALUES (1,'Deficiência intelectual',0.32,0.20),(2,'Face alongada/orelhas',0.29,0.09),(3,'Macroorquidismo',0.26,0.00),(4,'Hipermobilidade articular',0.19,0.04),(5,'Dificuldades de aprendizagem',0.18,0.28),(6,'Déficit de atenção',0.17,0.12),(7,'Movimentos repetitivos',0.17,0.05),(8,'Atraso na fala',0.14,0.01),(9,'Hiperatividade',0.12,0.04),(10,'Evita contato visual',0.06,0.08),(11,'Evita contato físico',0.04,0.07),(12,'Agressividade',0.01,0.02);
/*!40000 ALTER TABLE `sintoma` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(255) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `dataNascimento` date NOT NULL,
  `dataCriacao` datetime NOT NULL DEFAULT current_timestamp(),
  `permissao` enum('ADM','COM') NOT NULL,
  `fotoPerfil` varchar(255) DEFAULT NULL,
  `status` enum('Ativo','Inativo') DEFAULT 'Ativo',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user` (`user`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'admin','Alice','$2b$12$Pq3/Qu7ScipMZ6X3QMHMqOQpxS6BT4mWpne3nGNDh2.LIc8XxBv7a','1970-12-31','2026-05-27 00:00:00','ADM',NULL,'Ativo'),(2,'comum','Bob','$2b$12$Pq3/Qu7ScipMZ6X3QMHMqOQpxS6BT4mWpne3nGNDh2.LIc8XxBv7a','2002-02-02','2026-05-27 00:00:00','COM',NULL,'Ativo'),(3,'Rogerio','Rogerinho','$2b$12$PPd4gQNGRh/hfhIdOZ8dWuWGAjI3ZIfYvkQhrIU3j9YvIx5P8M6qC','1111-11-11','2026-06-13 08:42:24','COM',NULL,'Ativo');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-13  9:45:11

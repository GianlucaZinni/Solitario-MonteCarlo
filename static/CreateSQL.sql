-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Estrategia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Estrategia` (
  `idEstrategia` INT NOT NULL,
  `Nombre` VARCHAR(45) NOT NULL,
  `Descripcion` VARCHAR(200) NULL,
  PRIMARY KEY (`idEstrategia`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Games`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Games` (
  `idGames` INT NOT NULL AUTO_INCREMENT,
  `victoria` TINYINT NOT NULL,
  `duracion` INT NOT NULL,
  `Estrategia_idEstrategia` INT NOT NULL,
  PRIMARY KEY (`idGames`),
  INDEX `fk_Games_Estrategia_idx` (`Estrategia_idEstrategia` ASC) VISIBLE,
  CONSTRAINT `fk_Games_Estrategia`
    FOREIGN KEY (`Estrategia_idEstrategia`)
    REFERENCES `mydb`.`Estrategia` (`idEstrategia`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
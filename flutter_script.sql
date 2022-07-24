-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema flutter_schema
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `flutter_schema` ;

-- -----------------------------------------------------
-- Schema flutter_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `flutter_schema` DEFAULT CHARACTER SET utf8 ;
USE `flutter_schema` ;

-- -----------------------------------------------------
-- Table `flutter_schema`.`friends`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `flutter_schema`.`friends` (
  `idfriend` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`idfriend`),
  INDEX `fk_friends_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_friends_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `flutter_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `flutter_schema`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `flutter_schema`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `idfriend` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_users_friends1_idx` (`idfriend` ASC) VISIBLE,
  CONSTRAINT `fk_users_friends1`
    FOREIGN KEY (`idfriend`)
    REFERENCES `flutter_schema`.`friends` (`idfriend`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `flutter_schema`.`posts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `flutter_schema`.`posts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `content` VARCHAR(2000) NULL,
  `location` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `profile_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_posts_profiles1_idx` (`profile_id` ASC) VISIBLE,
  CONSTRAINT `fk_posts_profiles1`
    FOREIGN KEY (`profile_id`)
    REFERENCES `flutter_schema`.`profiles` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `flutter_schema`.`likes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `flutter_schema`.`likes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `post_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_likes_posts1_idx` (`post_id` ASC) VISIBLE,
  CONSTRAINT `fk_likes_posts1`
    FOREIGN KEY (`post_id`)
    REFERENCES `flutter_schema`.`posts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `flutter_schema`.`shares`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `flutter_schema`.`shares` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `post_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_shares_posts1_idx` (`post_id` ASC) VISIBLE,
  CONSTRAINT `fk_shares_posts1`
    FOREIGN KEY (`post_id`)
    REFERENCES `flutter_schema`.`posts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `flutter_schema`.`profiles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `flutter_schema`.`profiles` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `username` VARCHAR(255) NULL,
  `bio` VARCHAR(1000) NULL,
  `birthday` DATE NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `like_id` INT NULL DEFAULT NULL,
  `share_id` INT NULL DEFAULT NULL,
  `user_id` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_profiles_likes1_idx` (`like_id` ASC) VISIBLE,
  INDEX `fk_profiles_shares1_idx` (`share_id` ASC) VISIBLE,
  INDEX `fk_profiles_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_profiles_likes1`
    FOREIGN KEY (`like_id`)
    REFERENCES `flutter_schema`.`likes` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_profiles_shares1`
    FOREIGN KEY (`share_id`)
    REFERENCES `flutter_schema`.`shares` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_profiles_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `flutter_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `flutter_schema`.`comments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `flutter_schema`.`comments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `comment` VARCHAR(2000) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `post_id` INT NOT NULL,
  `profile_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_comments_posts1_idx` (`post_id` ASC) VISIBLE,
  INDEX `fk_comments_profiles1_idx` (`profile_id` ASC) VISIBLE,
  CONSTRAINT `fk_comments_posts1`
    FOREIGN KEY (`post_id`)
    REFERENCES `flutter_schema`.`posts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comments_profiles1`
    FOREIGN KEY (`profile_id`)
    REFERENCES `flutter_schema`.`profiles` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

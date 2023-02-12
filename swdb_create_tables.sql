

-- -----------------------------------------------------
-- Table `project_database_cs340`.`Media_Types`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Media_Types (
  media_type_id INT NOT NULL AUTO_INCREMENT,
  media_type VARCHAR(145) NOT NULL,
  PRIMARY KEY (media_type_id)
  );

-- -----------------------------------------------------
-- Table Media
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Media (
  media_id INT NOT NULL AUTO_INCREMENT,
  media_name VARCHAR(145) NOT NULL,
  media_type_id INT NOT NULL,
  release_year YEAR(4) NOT NULL,
  PRIMARY KEY (media_id),
  CONSTRAINT fk_Media_Media_Types1
    FOREIGN KEY (media_type_id)
    REFERENCES Media_Types(media_type_id)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table Regions
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Regions (
  region_id INT NOT NULL AUTO_INCREMENT,
  region_name VARCHAR(145) NOT NULL,
  PRIMARY KEY (region_id)
  );

-- -----------------------------------------------------
-- Table Planets
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Planets (
  planet_id INT NOT NULL AUTO_INCREMENT,
  planet_name VARCHAR(145) NOT NULL,
  region_id INT NOT NULL,
  description TEXT(65535) NULL,
  planet_first_appearance INT,
  PRIMARY KEY (planet_id),

  CONSTRAINT fk_planets_media_titles
    FOREIGN KEY (planet_first_appearance)
    REFERENCES Media (media_id)
    ON DELETE SET NULL
    ON UPDATE NO ACTION,

    CONSTRAINT fk_Planets_Regions1
    FOREIGN KEY (region_id)
    REFERENCES Regions (region_id)
    ON DELETE RESTRICT);



-- -----------------------------------------------------
-- Table Species
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Species (
  species_id INT NOT NULL AUTO_INCREMENT,
  classification VARCHAR(145) NOT NULL,
  species_home_planet INT NULL,
  PRIMARY KEY (species_id),

  CONSTRAINT fk_species_planet1
    FOREIGN KEY (species_home_planet)
    REFERENCES Planets (planet_id)
    ON DELETE SET NULL
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table Characters
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Characters (
  character_id INT NOT NULL AUTO_INCREMENT,
  character_name VARCHAR(145) NOT NULL,
  character_home_planet INT NULL,
  character_first_appearance INT NULL,
  species INT NOT NULL,
  birth_year VARCHAR(145) NULL,
  PRIMARY KEY (character_id),

  CONSTRAINT fk_characters_planets1
    FOREIGN KEY (character_home_planet)
    REFERENCES Planets (planet_id)
    ON DELETE SET NULL
    ON UPDATE NO ACTION,

  CONSTRAINT fk_characters_media_titles1
    FOREIGN KEY (character_first_appearance)
    REFERENCES Media (media_id)
    ON DELETE SET NULL
    ON UPDATE NO ACTION,

  CONSTRAINT fk_characters_species1
    FOREIGN KEY (Species)
    REFERENCES Species (species_id)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table Affiliations
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Affiliations (
  affiliation_id INT NOT NULL AUTO_INCREMENT,
  affiliation VARCHAR(145) NOT NULL,
  PRIMARY KEY (affiliation_id)
  );


-- -----------------------------------------------------
-- Table Character_Affiliations
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Character_Affiliations (
  affiliation_id INT NOT NULL,
  character_id INT NOT NULL,
  PRIMARY KEY (affiliation_id, character_id),
  
  CONSTRAINT fk_affiliations_has_characters_affiliations1
    FOREIGN KEY (affiliation_id)
    REFERENCES Affiliations (affiliation_id)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,

  CONSTRAINT fk_affiliations_has_characters_characters1
    FOREIGN KEY (character_id)
    REFERENCES Characters (character_id)
    ON DELETE CASCADE
    ON UPDATE NO ACTION);

-- -----------------------------------------------------
-- Table `project_database_cs340`.`Ship_Classifications`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Ship_Classifications (
  ship_classification_id INT NOT NULL AUTO_INCREMENT,
  ship_type VARCHAR(145) NOT NULL,
  PRIMARY KEY (ship_classification_id));

-- -----------------------------------------------------
-- Table Ships
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Ships (
  ship_id INT NOT NULL AUTO_INCREMENT,
  ship_name VARCHAR(145) NOT NULL,
  ship_type INT NOT NULL,
  PRIMARY KEY (ship_id),

  CONSTRAINT fk__Ships_Ship_Classifications1
  FOREIGN KEY(ship_type) 
  REFERENCES Ship_Classifications(ship_classification_id)
  ON DELETE RESTRICT
  ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table Character_Ships
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Character_Ships (
  character_id INT NOT NULL,
  ship_id INT NOT NULL,
  PRIMARY KEY (character_id, ship_id),

  CONSTRAINT fk_characters_has_ships_characters1
    FOREIGN KEY (character_id)
    REFERENCES Characters (character_id)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,

  CONSTRAINT fk_characters_has_ships_ships1
    FOREIGN KEY (ship_id)
    REFERENCES Ships (ship_id)
    ON DELETE CASCADE
    ON UPDATE NO ACTION);
/*
This DDL file includes the sql operations to create each table and import
sample starter data for the CS340 database project. This DDL is the beginnings
of what could be a much larger undertaking to cataloge the entire Star Wars universe.
*/

-- -----------------------------------------------------
-- Table Media_Types -- Read Only
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
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table Regions -- Read Only
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
    ON UPDATE CASCADE,

    CONSTRAINT fk_Planets_Regions1
    FOREIGN KEY (region_id)
    REFERENCES Regions (region_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE);

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
    ON UPDATE CASCADE);


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
    ON UPDATE CASCADE,

  CONSTRAINT fk_characters_media_titles1
    FOREIGN KEY (character_first_appearance)
    REFERENCES Media (media_id)
    ON DELETE SET NULL
    ON UPDATE CASCADE,

  CONSTRAINT fk_characters_species1
    FOREIGN KEY (Species)
    REFERENCES Species (species_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE);


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
    ON UPDATE CASCADE,

  CONSTRAINT fk_affiliations_has_characters_characters1
    FOREIGN KEY (character_id)
    REFERENCES Characters (character_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- Table Ship_Classifications - Read Only
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
  ON UPDATE CASCADE);


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
    ON UPDATE CASCADE,

  CONSTRAINT fk_characters_has_ships_ships1
    FOREIGN KEY (ship_id)
    REFERENCES Ships (ship_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- -----------------------------------------------------
-- INSERTS FOR READ ONLY TABLES
-- -----------------------------------------------------
INSERT INTO Media_Types (media_type)
VALUES
  ('Movie'),
  ('TV Series'),
  ('Novel'),
  ('Comic'),
  ('Video Game');

INSERT INTO Regions (region_name)
VALUES
('Deep Core'),
('Core Worlds'),
('Colonies'),
('Expasion Region'),
('Mid Rim'),
('Outer Rim Territories'),
('Wild Space'),
('Unknown Regions');

INSERT INTO Ship_Classifications (ship_type)
VALUES
('Yacht'),
('Starfighter'),
('Bomber'),
('Scout Vessel'),
('Transport'),
('Shuttle'),
('Gunship'),
('System Patrol Craft'),
('Freighter'),
('Capital Ship'),
('Starship'),
('Space Station');

-- -----------------------------------------------------
-- INSERTS sample entries
-- -----------------------------------------------------

INSERT INTO Media (media_name, media_type_id, release_year)
VALUES 
  (
    'Star Wars Episode IV: A New Hope', 
    (SELECT media_type_id FROM Media_Types WHERE Media_Types.media_type = 'Movie'), 
    '1977'
  ),
  (
    'The Mandalorian', 
    (SELECT media_type_id FROM Media_Types WHERE Media_Types.media_type = 'TV Series'), 
    '2019'
  ),
  (
    'Darth Vader #3', 
    (SELECT media_type_id FROM Media_Types WHERE Media_Types.media_type = 'Comic'), 
    '2015'
  ),
  (
    'Star Wars: From the Adventures of Luke Skywalker', 
    (SELECT media_type_id FROM Media_Types WHERE Media_Types.media_type = 'Novel'),  
    '1976'
  ),
  (
    'Star Wars: The Clone Wars', 
    (SELECT media_type_id FROM Media_Types WHERE Media_Types.media_type = 'TV Series'),  
    '2008'
  ),
  (
    'Star Wars Episode VI: Return of the Jedi, Special Edition', 
    (SELECT media_type_id FROM Media_Types WHERE Media_Types.media_type = 'Movie'),  
    '1997'
  );

INSERT INTO Planets (planet_name, region_id, Planets.description, planet_first_appearance)
VALUES 
  (
    'Tatooine', 
    (SELECT region_id FROM Regions WHERE Regions.region_name = 'Outer Rim Territories'),  
    "Tatooine was a sparsely inhabited circumbinary desert planet located in the 
    galaxy's Outer Rim Territories. Part of a binary star system, the planet orbited 
    two scorching suns, resulting in the world lacking the necessary surface water 
    to sustain large populations. As a result, many residents of the planet instead 
    drew water from the atmosphere via moisture farms. The planet also had little 
    surface vegetation.", 
    (SELECT media_id FROM Media WHERE Media.media_name = 'Star Wars: From the Adventures of Luke Skywalker')
  ),
  (
    'Mandalore', 
    (SELECT region_id FROM Regions WHERE Regions.region_name = 'Outer Rim Territories'), 
    "Outer Rim planet that is the homeworld of the Mandalorians torn by wars between 
    Mandalorians and Jedi and eventually purged by the Empire, scattering the few 
    Mandalorians throughout the galaxy (including Bo-Katan). Mandalore has one moon, 
    Concordia, which is fully inhabited.",
    5
  ),
  (
    'Nevarro', 
    (SELECT region_id FROM Regions WHERE Regions.region_name = 'Outer Rim Territories'), 
    NULL,
    (SELECT media_id FROM Media WHERE Media.media_name = 'The Madalorian')
  ),
  (
    'Coruscant', 
    (SELECT region_id FROM Regions WHERE Regions.region_name = 'Outer Rim Territories'), 
    "Coruscant (pronounced /'kɔɹəsɑnt/), also known as Imperial Center during the rule 
    of the Galactic Empire, was an ecumenopolis—a city-covered planet, collectively 
    known as Imperial City— in the Coruscant system of the Core Worlds. Though debated 
    by historians, it was generally believed that Coruscant was the original homeworld 
    of humanity. Coruscant was at one point also historically the home of the ancient 
    Taung and Zhell. Noted for its cosmopolitan culture and towering skyscrapers, 
    Coruscant's population consisted of trillions of citizens hailing from a vast array 
    of both humanoid and alien species.",
    (SELECT media_id FROM Media WHERE Media.media_name = 'Star Wars Episode VI: Return of the Jedi, Special Edition')
  );

INSERT INTO Species(classification, species_home_planet)
VALUES
(
  'Human',
  (SELECT planet_id FROM Planets WHERE Planets.planet_name = 'Coruscant')
),
(
  'Wookie',
  NULL
),

(
  'Droid',
  (SELECT planet_id FROM Planets WHERE Planets.planet_name = 'Coruscant')
);

INSERT INTO Characters (character_name, character_home_planet, character_first_appearance, species, birth_year)
VALUES
(
  'Luke Skywalker',
  (SELECT planet_id From Planets where Planets.planet_name = 'Tatooine'),
  (SELECT media_id FROM Media WHERE Media.media_name = 'Star Wars: From the Adventures of Luke Skywalker' AND Media.release_year = 1976),
  (SELECT species_id FROM Species WHERE Species.classification = 'Human'),
  '19BBY'
),
(
  'Owen Lars',
  (SELECT planet_id From Planets where Planets.planet_name = 'Tatooine'),
  (SELECT media_id FROM Media WHERE Media.media_name = 'Star Wars Episode IV: A New Hope' AND Media.release_year = 1977),
  (SELECT species_id FROM Species WHERE Species.classification = 'Human'),
  NULL
),
(
  'Chewbacca',
  NULL,
  NULL,
  (SELECT species_id FROM Species WHERE Species.classification = 'Wookie'),
  '200BBY'
);

INSERT INTO Affiliations (affiliation)
VALUES 
('Rebel Alliance'),
('Galatic Empire'),
('Jedi Order'),
('Hutt Cartel');


INSERT INTO Ships (ship_name, ship_type)
VALUES
  (
    'Millenium Falcon', 
    (SELECT ship_classification_id FROM Ship_Classifications WHERE Ship_Classifications.ship_type = 'Freighter')
  ),
  (
    'Red Five', 
    (SELECT ship_classification_id FROM Ship_Classifications WHERE Ship_Classifications.ship_type = 'Starfighter')
  ),
  (
    'Breha', 
    (SELECT ship_classification_id FROM Ship_Classifications WHERE Ship_Classifications.ship_type = 'Starship')
  ),
  (
    'Red Three', 
    (SELECT ship_classification_id FROM Ship_Classifications WHERE Ship_Classifications.ship_type = 'Starfighter')
  );

INSERT INTO Character_Affiliations(affiliation_id, character_id)
VALUES
  (
    (SELECT affiliation_id FROM Affiliations WHERE Affiliations.affiliation = 'Rebel Alliance'), 
    (SELECT character_id from Characters WHERE Characters.character_name = 'Luke Skywalker')
  ),
  (
    (SELECT affiliation_id FROM Affiliations WHERE Affiliations.affiliation = 'Rebel Alliance'), 
    (SELECT character_id from Characters WHERE Characters.character_name = 'Chewbacca')
  ),
  (
    (SELECT affiliation_id FROM Affiliations WHERE Affiliations.affiliation = 'Jedi Order'),  
    (SELECT character_id from Characters WHERE Characters.character_name = 'Luke Skywalker')
  );

INSERT INTO Character_Ships(character_id, ship_id)
VALUES
  (
    (SELECT character_id from Characters WHERE Characters.character_name = 'Luke Skywalker'), 
    (SELECT ship_id from Ships WHERE Ships.ship_name = 'Millenium Falcon') 
  ),
  (
    (SELECT character_id from Characters WHERE Characters.character_name = 'Chewbacca'),  
    (SELECT ship_id from Ships WHERE Ships.ship_name = 'Millenium Falcon') 
  ),
  (
    (SELECT character_id from Characters WHERE Characters.character_name = 'Luke Skywalker'), 
    (SELECT ship_id from Ships WHERE Ships.ship_name = 'Red Five') 
  ),
  (
    (SELECT character_id from Characters WHERE Characters.character_name = 'Luke Skywalker'),  
    (SELECT ship_id from Ships WHERE Ships.ship_name = 'Breha') 
  );
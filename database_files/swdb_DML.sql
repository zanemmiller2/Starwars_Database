/* 
----------- SELECT Statements for Browse Pages -----------
                      (READ)
*/ 

-- Get all Media_Types
SELECT media_type_id, media_type FROM Media_Types;

-- Get all Media and their types
SELECT media_id, media_name AS Title, Media_Types.media_type AS 'Media Type', release_year AS 'Release Year' 
  FROM Media 
    INNER JOIN Media_Types 
      ON Media.media_type_id = Media_Types.media_type_id;

-- Get all Regions
SELECT region_id, region_name AS 'Region Name' FROM Regions;

-- Get all Planets, their regions, and first appearances
SELECT planet_id, planet_name AS 'Planet Name', Regions.region_name AS 'Region Name', description AS Description, Media.media_name AS 'First Media Appearance', Media.release_year AS 'Year'
  FROM Planets
    INNER JOIN Regions
      ON Planets.region_id = Regions.region_id
      LEFT JOIN Media
        ON Planets.planet_first_appearance = Media.media_id;

-- Get all Species and their home planets
SELECT species_id, classification AS 'Species Classification', Planets.planet_name AS 'Species Planet of Origin'
  FROM Species
    LEFT JOIN Planets
      ON species_home_planet = Planets.planet_id;

-- Get all Characters, their first appearances, their home planet and their species
SELECT character_id AS 'Character ID', character_name AS 'Character Name', Planets.planet_name AS 'Character Home Planet', Media.media_name AS 'First Media Appearance', Species.classification AS 'Character Species', birth_year AS 'Birth Year'
  FROM Characters
    LEFT JOIN Planets
      ON character_home_planet = Planets.planet_id
    LEFT JOIN Species
      ON species = Species.species_id
    LEFT JOIN Media
      ON character_first_appearance = media.media_id;

-- Get all Affiliations
SELECT affiliation_id, affiliation AS 'Affiliation' FROM Affiliations;

-- Get all Ship and their classifications

SELECT ship_id, ship_name AS 'Ship Name', Ship_Classifications.ship_type AS 'Ship Classification' 
  FROM Ships
    INNER JOIN Ship_Classifications 
      ON Ships.ship_type = Ship_Classifications.ship_classification_id;

-- Get all Ship Classifications
SELECT ship_classification_id, ship_type AS 'Ship Classification' FROM Ship_Classifications;

-- Get all Character Ships
SELECT characters.character_name AS 'Character Name', ships.ship_name AS 'Ship Name'
  FROM characters
    JOIN character_ships ON character_ships.character_id = characters.character_id
    JOIN ships ON ships.ship_id = character_ships.ship_id;

-- Get all Character Affiliations
SELECT characters.character_name AS 'Character Name', affiliations.affiliation AS 'Affiliation Name'
  FROM characters
    JOIN character_affiliations ON character_affiliations.character_id = characters.character_id
    JOIN affiliations ON affiliations.affiliation_id = character_affiliations.affiliation_id;

/* -----------------------------------------------
----------- DML Statements for Inserts -----------
                      (Create)
------------------------------------------------ */ 

-- Insert new Media
INSERT INTO Media (media_name, media_type_id, release_year) 
  VALUES 
    (:media_name, :media_type_id_from_drop_down_input, :release_year);

-- Insert new Planet
INSERT INTO Planets (planet_name, region_id, description, planet_first_appearance)
  VALUES 
    (:planet_name, :region_id_from_drop_down_input, :description, :media_id_from_drop_down_input);

-- Insert new Species
INSERT INTO Species (classification, species_home_planet)
  VALUES
    (:classification, :planet_id_selected_from_drop_down_input)

-- Insert new Media_Type
INSERT INTO Media_Types (media_type)
  VALUES
    (:media_type);

-- Insert new Regions
INSERT INTO Regions (region_name)
  VALUES
    (:region_name);
  
-- Insert new Character
INSERT INTO Characters (character_name, character_home_planet, character_first_appearance, species, birth_year)
  VALUES
    (:character_name, :planet_id_from_drop_down_input, :media_id_from_drop_down_input, :species_id_from_drop_down_input, :birth_year);

-- Insert into Affiliations
INSERT INTO Affiliations (affiliation)
  VALUES
    (:affiliation);

-- Insert into Ships
INSERT INTO Ships (ship_name, ship_type)
  VALUES
    (:ship_name,:ship_classification_from_drop_down_input);

-- Insert into Ships Classifications
INSERT INTO Ship_Classifications (ship_type)
  VALUES
    (:ship_type);

-- Insert into Character Ships
INSERT INTO Character_Ships (character_id, ship_id)
  VALUES
    (:character_id_from_drop_down_input,:ship_id_from_drop_down_input);

-- Insert into Character Affiliations
INSERT INTO Character_Affiliations (character_id, affiliation_id)
  VALUES
    (:character_id_from_drop_down_input,:affiliation_id_from_drop_down_input);
/* -----------------------------------------------
----------- DML Statements for Deletes -----------
                      (Delete)
------------------------------------------------ */ 
-- Delete Media record
DELETE FROM Media WHERE media_id = :media_id_from_browse_media_page;

-- Delete Planet
DELETE FROM Planets WHERE planet_id = :planet_id_selected_browse_planet_page;

-- Delete Species
DELETE FROM Species WHERE species_id = :species_id_from_browse_species_page;

-- Delete Characters
DELETE FROM Characters WHERE character_id = :character_id_from_browse_characters_page;

-- Delete Ships
DELETE FROM Ships WHERE ship_id = :ship_id_from_browse_ships_page;

-- Delete Affiliations
DELETE FROM Affiliations WHERE affiliation_id = :affiliation_id_from_browse_affiliations_page;

-- Delete Character Affiliation
DELETE FROM Ship_Classifications WHERE ship_classification_id = :ship_classification_id_from_browse_ship_classifications_page;

/* -----------------------------------------------
----------- DML Statements for Updates -----------
                      (Update)
------------------------------------------------ */ 
-- Update Media Record from user submission
UPDATE Media  
  SET media_name = :media_name_input, 
      media_type_id = :media_type_id_from_drop_down_input, 
      release_year = :release_year
  WHERE media_id = :media_id_selected_from_browse_media_page;

-- Update Planet
UPDATE Planets  
  SET planet_name = :planet_name_input, 
      region_id = :region_id_from_drop_down_input, 
      planets.description = :description_input,
      planet_first_appearance = :media_id_from_drop_down_input
  WHERE planet_id = :planet_id_selected_from_browse_planets_page;

-- Update Species
UPDATE Species
  SET
    classification = :classification_input,
    species_home_planet = :planet_id_selected_from_drop_down_input
  WHERE species_id = :species_id_selected_from_browse_species_page;

-- Update Regions
UPDATE Regions
  SET
    region_name = :region_name_input
  WHERE region_id = :region_id_selected_from_browse_regions_page;

-- Update Media_Types
UPDATE Media_Types
  SET
    media_type = :media_type_input
  WHERE media_type_id = :media_type_id_selected_from_browse_media_types_page;

-- Update Characters
UPDATE Characters
  SET
    character_name = :character_name_input,
    character_home_planet = :planet_id_from_drop_down_input,
    character_first_appearance = :media_id_from_drop_down_input,
    species = :species_id_from_drop_down_input,
    birth_year = :birth_year_input
  WHERE character_id = :character_id_selected_from_browse_character_page;

-- Update Affiliations
UPDATE Affiliations
  SET
    affiliation = :affiliation_input
  WHERE affiliation_id = :affiliation_id_selected_from_browse_affiliation_page;

-- Update Ships
UPDATE Ships
  SET
    ship_name = :ship_name_input,
    ship_type = :ship_classification_id_selected_from_drop_down_input
  WHERE ship_id = :ship_id_selected_from_browse_ships_page;

-- Update Ship Classifications
UPDATE Ship_Classifications
  SET
    ship_type = :ship_type_input
  WHERE ship_classification_id = :ship_classification_id_from_browse_ship_classifications_page;

/* ------------------------------------------
Queries for search bars

------------------------------------------- */
-- Search/Filter Planets
SELECT planet_id, planet_name AS 'Planet Name', Regions.region_name AS 'Region Name', description AS Description, Media.media_name AS 'First Media Appearance', Media.release_year AS 'Year'
  FROM Planets
    INNER JOIN Regions
      ON Planets.region_id = Regions.region_id
      LEFT JOIN Media
        ON Planets.planet_first_appearance = Media.media_id
    WHERE planet_name LIKE %:search_parameter% OR Regions.region_name LIKE %:search_parameter% OR Media.media_name LIKE %:search_parameter% OR Media.release_year LIKE %:search_parameter%;

-- Search/Filter Planets with null values
SELECT planet_id, planet_name AS 'Planet Name', Regions.region_name AS 'Region Name', description AS Description, Media.media_name AS 'First Media Appearance', Media.release_year AS 'Year'
  FROM Planets
    INNER JOIN Regions
      ON Planets.region_id = Regions.region_id
      LEFT JOIN Media
        ON Planets.planet_first_appearance = Media.media_id
    WHERE planet_nameIS NULL OR Regions.region_name IS NULL OR Media.media_name IS NULL OR Media.release_year IS NULL;


/* ------------------------------------------
Queries for drop down menus and selecting ids 
for updates and deletes 
------------------------------------------- */

-- Select Media Record based on submission from Update Media form
-- media_id_selected_from_browse_media_page
SELECT media_id, media_name, media_type_id, release_year 
  FROM Media
    WHERE media_id = :media_id_selected_from_browse_media_page;

-- Select Regions Record based on submission from Update Regions form
-- region_id_selected_from_browse_region_page
SELECT region_id, region_name
  FROM Regions
    WHERE region_id = :region_id_selected_from_browse_regions_page;

-- Select Planet Record based on submission from Update Planet form
-- planet_id_selected_from_browse_planets_page
SELECT planet_id, planet_name, region_id, description, planet_first_appearance
  FROM Planets
    WHERE planet_id = :planet_id_selected_from_browse_planets_page;

-- Select Species Record based on submission from Browse Species page
-- species_id_from_browse_species_page
SELECT species_id, classification, species_home_planet
  FROM Species
    WHERE species_id = :species_id_selected_from_browse_species_page;

-- Select Media_Types Record based on submission from Browse Media_Types page
-- media_type_id_selected_from_browse_media_types_page
SELECT media_type_id, media_type
  FROM Media_Types
    WHERE media_type_id = :media_type_id_selected_from_browse_media_types_page;

-- Select Affiliation based on submission from Browse Affiliation page
SELECT affiliation_id, affiliation
  FROM Affiliations
    WHERE affiliation_id = :affiliation_id_selected_from_browse_affiliation_page;

-- Select Characters based on submission from Browse Characters page
SELECT character_id, character_name, character_home_planet, character_first_appearance, species, birth_year
  FROM Characters
    WHERE character_id = :character_id_selected_from_browse_character_page;

-- Select Ships based on submission from Browse Ship page
SELECT ship_id, ship_name, ship_type
  FROM Ships
    WHERE ship_id = :ship_id_selected_from_browse_ships_page;

-- Select Ship Classification based on submission from Browse Ship Classification page
SELECT ship_classification_id, ship_type
  FROM  Ship_Classifications
    WHERE ship_classification_id = :ship_classification_id_selected_from_drop_down_input;

-- Get all Regions to populate Regions type drop downs and pass FK INT region_id_from_drop_down_input
-- region_id_from_drop_down_input
SELECT region_id, region_name from Regions;

-- Get all Media_Types to populate Media type drop downs and pass FK INT media_type_id_from_drop_down_input
-- media_type_id_from_drop_down_input
SELECT media_type_id, media_type from Media_Types;

-- Get all Planets to populate planets drop down list
-- planet_id_selected_from_drop_down_input
SELECT planet_id, planet_name from Planets;

-- Get all Ship Classifications to populate ship classifications drop down list
SELECT ship_classification_id, ship_type from Ship_Classifications;

-- Get all affiliations to populate affiliations drop down list
SELECT affiliation_id, affiliation from Affiliations;


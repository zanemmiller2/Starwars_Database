"""
Sources: app.py, db_connecter.py, db_credentials.py and template pages adopted
from exploration starter code bsg_app
"""
from time import sleep

from flask import Flask, render_template, json, request, redirect, url_for, flash
from flask_navigation import Navigation
import os

import database.db_connector as db
import pymysql

# Configuration
app = Flask(__name__)
app.secret_key = "secret key"

nav = Navigation(app)
nav.Bar('top', [
        nav.Item('Home', 'index'),
        nav.Item('Planets', 'browse_planets'),
        nav.Item('Regions', 'browse_regions'),
        nav.Item('Media', 'browse_media'),
        nav.Item('Media Types', 'browse_media_types'),
        nav.Item('Species', 'browse_species'),
        nav.Item('Characters', 'browse_characters'),
        nav.Item('Ships', 'browse_ships'),
        nav.Item('Affiliations', 'browse_affiliations'),
        nav.Item('Character Ships', 'browse_character_ships'),
        nav.Item('Ship Classifications',
                 'browse_ships_classifications'),
        nav.Item('Character Affiliations',
                 'browse_character_affiliations')]
        )


# Routes
@app.route('/')
def index():
    """ App home page """
    return render_template("index.html")


@app.route('/search-planets', methods=["POST"])
def search_planets():
    """
    function executes the search parameters from the search bar on planets page
    """

    search_parameter = request.form["search_parameter"].title()

    # Search fields with null values
    if search_parameter.lower() == 'none' or search_parameter.lower() == 'null':
        planet_by_name_count_query = "SELECT planet_id AS 'Planet ID', planet_name AS 'Planet Name', " \
                                     "Regions.region_name AS 'Region Name', " \
                                     "description AS Description, " \
                                     "Media.media_name AS 'First Media Appearance', " \
                                     "Media.release_year AS 'Year' " \
                                     "FROM Planets INNER JOIN Regions " \
                                     "ON Planets.region_id = Regions.region_id " \
                                     "LEFT JOIN Media " \
                                     "ON Planets.planet_first_appearance = Media.media_id " \
                                     "WHERE planet_name IS NULL " \
                                     "OR description IS NULL " \
                                     "OR Regions.region_name IS NULL " \
                                     "OR Media.media_name IS NULL " \
                                     "OR Media.release_year IS NULL;"
        db_connection = db.connect_to_database()
        search_data = db.execute_query(db_connection,
                                       planet_by_name_count_query).fetchall()
        db_connection.close()

    # search planets table for partial matches in any parameter
    elif search_parameter:
        search_parameter = '%' + search_parameter + '%'
        planet_by_name_count_query = "SELECT planet_id AS 'Planet ID', planet_name AS 'Planet Name', " \
                                     "Regions.region_name AS 'Region Name', " \
                                     "description AS Description, " \
                                     "Media.media_name AS 'First Media Appearance', " \
                                     "Media.release_year AS 'Year' " \
                                     "FROM Planets INNER JOIN Regions " \
                                     "ON Planets.region_id = Regions.region_id " \
                                     "LEFT JOIN Media " \
                                     "ON Planets.planet_first_appearance = Media.media_id WHERE planet_name LIKE %s OR description LIKE %s OR Regions.region_name LIKE %s OR Media.media_name LIKE %s OR Media.release_year LIKE %s;"

        db_connection = db.connect_to_database()
        search_data = db.execute_query(db_connection,
                                       planet_by_name_count_query,
                                       (search_parameter, search_parameter, search_parameter,
                                        search_parameter,
                                        search_parameter)).fetchall()
        db_connection.close()

    # empty search - reset the page
    else:
        return redirect('/planets')

    # get remaining values for rendering the updated table after search/filter
    regions_query = "SELECT region_id, region_name FROM Regions;"
    db_connection = db.connect_to_database()
    regions_data = db.execute_query(db_connection,
                                    regions_query).fetchall()
    db_connection.close()

    media_types_query = "SELECT media_type_id, media_type FROM Media_Types;"
    db_connection = db.connect_to_database()
    media_types_data = db.execute_query(db_connection,
                                        media_types_query).fetchall()
    db_connection.close()

    media_query = "SELECT media_id, media_name FROM Media;"
    db_connection = db.connect_to_database()
    media_data = db.execute_query(db_connection, media_query).fetchall()
    db_connection.close()

    return render_template("planets.html",
                           planets=search_data,
                           regions=regions_data,
                           media_types=media_types_data,
                           media=media_data)


@app.route('/planets', methods=["POST", "GET"])
def browse_planets():
    """ Page to browse planets"""
    if request.method == 'GET':
        select_query = "SELECT planet_id AS 'Planet ID', planet_name AS 'Planet Name', " \
                       "Regions.region_name AS 'Region Name', " \
                       "description AS Description, " \
                       "Media.media_name AS 'First Media Appearance', " \
                       "Media.release_year AS 'Year' " \
                       "FROM Planets INNER JOIN Regions " \
                       "ON Planets.region_id = Regions.region_id " \
                       "LEFT JOIN Media " \
                       "ON Planets.planet_first_appearance = Media.media_id;"
        db_connection = db.connect_to_database()
        planet_data = db.execute_query(db_connection, select_query).fetchall()
        db_connection.close()

        # For the insert form
        regions_query = "SELECT region_id, region_name FROM Regions;"
        db_connection = db.connect_to_database()
        regions_data = db.execute_query(db_connection,
                                        regions_query).fetchall()
        db_connection.close()

        media_types_query = "SELECT media_type_id, media_type FROM Media_Types;"
        db_connection = db.connect_to_database()
        media_types_data = db.execute_query(db_connection,
                                            media_types_query).fetchall()
        db_connection.close()

        media_query = "SELECT media_id, media_name FROM Media;"
        db_connection = db.connect_to_database()
        media_data = db.execute_query(db_connection, media_query).fetchall()
        db_connection.close()

        return render_template("planets.html",
                               planets=planet_data,
                               regions=regions_data,
                               media_types=media_types_data,
                               media=media_data)

    # Insert a new planet
    elif request.method == 'POST':

        planet_name = request.form["planet_name"]
        region_id = int(request.form["region"])
        media_id = int(request.form["media_id"])

        # get the description data if there is any
        if request.form["planet_description"] != "" and request.form["planet_description"] != "None":
            description = request.form["planet_description"]

        # set description to null if there is no description entered by the
        # user
        else:
            description = "NULL"

        get_region_name_query = "SELECT region_id, region_name " \
                                "FROM Regions WHERE region_id=%s;"
        get_region_name_query_params = (region_id,)
        db_connection = db.connect_to_database()
        region_data = db.execute_query(db_connection,
                                       get_region_name_query,
                                       get_region_name_query_params).fetchall()
        db_connection.close()

        # Add new media and then add entry to database
        if media_id == -2:
            return redirect(url_for('add_planet_and_media',
                                    new_planet_name=planet_name,
                                    region_id=region_data[0]["region_id"],
                                    region_name=region_data[0]["region_name"],
                                    description=description))

        # Optional Null first appearance - insert new planet with remaining details
        elif media_id == -1:

            # Not null description
            if description != "NULL":
                planet_insert_query = "INSERT INTO Planets " \
                                      "(planet_name, region_id, description) " \
                                      "VALUES (%s, %s, %s);"
                planet_insert_query_params = (
                        planet_name, region_id, description)

            # null description
            else:
                planet_insert_query = "INSERT INTO Planets " \
                                      "(planet_name, region_id, description) " \
                                      "VALUES (%s, %s, NULL);"
                planet_insert_query_params = (
                        planet_name, region_id)

            db_connection = db.connect_to_database()
            db.execute_query(db_connection, planet_insert_query,
                             planet_insert_query_params)
            db_connection.close()

        # insert new planet with first_appearance selection
        else:
            # Not null description
            if description != "NULL":
                planet_insert_query = "INSERT INTO Planets " \
                                      "(planet_name, region_id, " \
                                      "description, planet_first_appearance) " \
                                      "VALUES (%s, %s, %s, %s);"
                planet_insert_query_params = (
                        planet_name, region_id, description, media_id)

            # null description
            else:
                planet_insert_query = "INSERT INTO Planets " \
                                      "(planet_name, region_id, " \
                                      "description, planet_first_appearance) " \
                                      "VALUES (%s, %s, NULL, %s);"
                planet_insert_query_params = (
                        planet_name, region_id, media_id)


            db_connection = db.connect_to_database()
            db.execute_query(db_connection,
                             planet_insert_query,
                             planet_insert_query_params)
            db_connection.close()

        return redirect('/planets')


@app.route('/add-planet-and-media', methods=["POST", "GET"])
def add_planet_and_media():
    # Adding new media and new planet
    if request.method == 'POST':
        media_name = request.form["new_media_name"].title()
        media_type_id = int(request.form["media_type_id"])
        release_year = str(request.form["year"])
        planet_name = request.form["planet_name"]
        planet_region_id = int(request.form["region_id"])


        # get the description data if there is any
        if request.form["planet_description"] != "" and request.form["planet_description"] != "None":
            planet_description = request.form["planet_description"]
        # set description to null if there is no description entered by the
        # user
        else:
            planet_description = "NULL"

        # double check the new media isnt already in the db
        find_matching_movies_query = "SELECT media_id, media_name " \
                                     "FROM Media " \
                                     "WHERE media_name=%s AND release_year=%s;"
        find_matching_movies_query_params = (media_name, release_year)
        db_connection = db.connect_to_database()
        matches = db.execute_query(db_connection,
                                   find_matching_movies_query,
                                   find_matching_movies_query_params).fetchall()
        db_connection.close()

        count_matches = len(matches)

        # Insert media if it is not already present
        if count_matches == 0:
            # First insert new media
            insert_new_media_query = "INSERT INTO Media " \
                                     "(media_name, media_type_id, release_year) " \
                                     "VALUES (%s, %s, %s);"
            insert_new_media_query_params = (
                    media_name,
                    media_type_id,
                    release_year)
            db_connection = db.connect_to_database()
            cursor = db.execute_query(db_connection,
                                      insert_new_media_query,
                                      insert_new_media_query_params)
            media_id = cursor.lastrowid
            db_connection.close()

        else:
            media_id = int(matches[0]['media_id'])

        # Then insert new planet
        if planet_description != "NULL":
            insert_new_planet_query = "INSERT INTO Planets (" \
                                      "planet_name, " \
                                      "region_id, " \
                                      "description, " \
                                      "planet_first_appearance) " \
                                      "VALUES (%s, %s, %s, %s);"
            insert_new_planet_query_params = (
                    planet_name, planet_region_id, planet_description, media_id)

        else:
            insert_new_planet_query = "INSERT INTO Planets (" \
                                      "planet_name, " \
                                      "region_id, " \
                                      "description, " \
                                      "planet_first_appearance) " \
                                      "VALUES (%s, %s, NULL, %s);"
            insert_new_planet_query_params = (
                    planet_name, planet_region_id,
                    media_id)

        db_connection = db.connect_to_database()
        db.execute_query(db_connection,
                         insert_new_planet_query,
                         insert_new_planet_query_params)
        db_connection.close()

        return redirect('/planets')

    # get data for displaying values in add media form field
    elif request.method == 'GET':
        media_types_query = "SELECT media_type_id, media_type FROM Media_Types;"
        db_connection = db.connect_to_database()
        media_types_data = db.execute_query(db_connection,
                                            media_types_query).fetchall()
        db_connection.close()

        planet_name = request.args.get("new_planet_name")
        region_id = int(request.args.get("region_id"))
        region_name = request.args.get("region_name")
        description = request.args.get("description")
        return render_template('add_planet_and_media.html',
                               media_types=media_types_data,
                               new_planet_name=planet_name,
                               region_id=region_id,
                               region_name=region_name,
                               description=description)


@app.route('/edit_planet/<int:id>', methods=["POST", "GET"])
def edit_planet(id):
    # get data for displaying prefilled form fields on edit page
    if request.method == "GET":
        planet_query = "SELECT planet_id, Planets.region_id, " \
                       "Planets.planet_first_appearance, " \
                       "planet_name AS 'Planet Name', " \
                       "Regions.region_name AS 'Region Name', " \
                       "description AS Description, " \
                       "Media.media_name AS 'First Media Appearance', " \
                       "Media.release_year AS 'Year' " \
                       "FROM Planets INNER JOIN Regions " \
                       "ON Planets.region_id = Regions.region_id " \
                       "LEFT JOIN Media " \
                       "ON Planets.planet_first_appearance = Media.media_id " \
                       "WHERE planet_id=%s;"
        planet_query_params = (id,)
        db_connection = db.connect_to_database()
        planet_data = db.execute_query(
                db_connection,
                planet_query,
                planet_query_params).fetchall()
        db_connection.close()

        # Get values for drop down menus
        regions_dropdown_query = "SELECT region_id, region_name from Regions;"
        db_connection = db.connect_to_database()
        regions_dropdown = db.execute_query(db_connection,
                                            regions_dropdown_query).fetchall()
        db_connection.close()

        first_appearances_dropdown_query = "SELECT * from Media;"
        db_connection = db.connect_to_database()
        first_appearances_dropdown = db.execute_query(
                db_connection,
                first_appearances_dropdown_query).fetchall()
        db_connection.close()

        media_types_query = "SELECT media_type_id, media_type FROM Media_Types;"
        db_connection = db.connect_to_database()
        media_types_data = db.execute_query(db_connection,
                                            media_types_query).fetchall()
        db_connection.close()

        return render_template('edit_planet.html', planet_data=planet_data,
                               regions_dropdown=regions_dropdown,
                               first_appearance=first_appearances_dropdown,
                               media_types=media_types_data)

    # Edit the planet with the form entry values
    if request.method == "POST":
        planet_name = request.form["planet_name"]
        planet_id = request.form["planet_id"]
        planet_region = int(request.form["planet_region_id"])
        first_appearance = int(request.form["update_media_id"])
        year = request.form["update_year"]

        # get the description data if there is any
        if request.form["update_description"] != "" and request.form["update_description"] != "None":
            planet_description = request.form["update_description"]

        # set description to null if there is no description entered by the
        # user
        else:
            planet_description = "NULL"

        # Null first appearance
        if first_appearance == -1:
            if planet_description != "NULL":
                edit_planet_query = "UPDATE Planets SET planet_name=%s, region_id=%s, " \
                                    "description=%s, planet_first_appearance=NULL " \
                                    "WHERE planet_id=%s;"
                edit_planet_query_params = (
                        planet_name, planet_region, planet_description,
                        planet_id)

            else:
                edit_planet_query = "UPDATE Planets SET planet_name=%s, region_id=%s, " \
                                    "description=NULL, planet_first_appearance=NULL " \
                                    "WHERE planet_id=%s;"
                edit_planet_query_params = (
                        planet_name, planet_region, planet_id)

        else:
            if planet_description != "NULL":
                edit_planet_query = "UPDATE Planets SET planet_name=%s, region_id=%s, " \
                                    "description=%s, planet_first_appearance=%s " \
                                    "WHERE planet_id=%s;"
                edit_planet_query_params = (
                        planet_name, planet_region, planet_description,
                        first_appearance,
                        planet_id)
            else:
                edit_planet_query = "UPDATE Planets SET planet_name=%s, region_id=%s, " \
                                    "description=NULL, planet_first_appearance=%s " \
                                    "WHERE planet_id=%s;"
                edit_planet_query_params = (
                        planet_name, planet_region,
                        first_appearance,
                        planet_id)


        db_connection = db.connect_to_database()
        db.execute_query(db_connection,
                         edit_planet_query, edit_planet_query_params)
        db_connection.close()

        return redirect("/planets")


@app.route('/delete_planet/<int:id>', methods=["POST", "GET"])
def delete_planet(id):
    # Display Are you sure you want to delete the planet? page with record to
    # be deleted.
    if request.method == "GET":
        planet_query = "SELECT planet_id, planet_name from Planets " \
                       "WHERE planet_id=%s;"
        planet_query_params = (id,)
        db_connection = db.connect_to_database()
        planet_data = db.execute_query(
                db_connection,
                planet_query,
                planet_query_params).fetchall()
        db_connection.close()

        return render_template('delete_planet.html', planet_data=planet_data)

    # Delete the planet
    if request.method == "POST":
        planet_id = int(request.form["planet_id"])
        delete_planet_query = "DELETE FROM Planets WHERE planet_id=%s;"
        delete_planet_query_params = (planet_id,)
        db_connection = db.connect_to_database()
        db.execute_query(db_connection,
                         delete_planet_query, delete_planet_query_params)
        db_connection.close()

        return redirect("/planets")


@app.route('/media', methods=["POST", "GET"])
def browse_media():
    # Page for browsing all media
    if request.method == 'GET':
        media_select_query = "SELECT media_id AS 'ID', media_name AS 'Title', " \
                             "Media_Types.media_type AS 'Media Type', release_year " \
                             "AS 'Release Year' FROM Media INNER JOIN Media_Types " \
                             "ON Media.media_type_id = Media_Types.media_type_id;"

        db_connection = db.connect_to_database()
        media_data = db.execute_query(db_connection,
                                      media_select_query).fetchall()
        db_connection.close()

        # drop-down to be used on add new media page
        media_types_query = "SELECT media_type_id, media_type FROM Media_Types;"

        db_connection = db.connect_to_database()
        media_types_data = db.execute_query(db_connection,
                                            media_types_query).fetchall()
        db_connection.close()

        return render_template("media.html", medias=media_data,
                               media_types=media_types_data)

    # Add new media record
    if request.method == "POST":
        media_name = request.form["media_name"]
        media_type_id = int(request.form["media_type_id"])
        release_year = request.form["year"]

        insert_new_media_query = "INSERT INTO Media " \
                                 "(media_name, media_type_id, release_year) " \
                                 "VALUES (%s, %s, %s)"
        insert_params = (media_name, media_type_id, release_year)
        db_connection = db.connect_to_database()
        db.execute_query(db_connection,
                         insert_new_media_query, insert_params).fetchall()
        db_connection.close()

        return redirect("/media")


@app.route('/edit_media/<int:id>', methods=["POST", "GET"])
def edit_media(id):
    # Display the media entry to edit
    if request.method == "GET":
        media_query = "SELECT media_id, Media.media_type_id," \
                      "media_name AS 'Title', " \
                      "Media_Types.media_type AS 'Media Type', " \
                      "release_year 'Release Year' " \
                      "FROM Media INNER JOIN Media_Types " \
                      "ON Media.media_type_id = Media_Types.media_type_id " \
                      "WHERE media_id=%s;"
        media_query_params = (id,)
        db_connection = db.connect_to_database()
        media_data = db.execute_query(
                db_connection,
                media_query,
                media_query_params).fetchall()
        db_connection.close()

        media_types_query = "SELECT media_type_id, media_type FROM Media_Types;"
        db_connection = db.connect_to_database()
        media_types_data = db.execute_query(db_connection,
                                            media_types_query).fetchall()
        db_connection.close()

        return render_template('edit_media.html', media_data=media_data,
                               media_types=media_types_data)

    # Update the media entry in the DB
    if request.method == "POST":
        media_title = request.form["media_title"]
        media_id = request.form["media_id"]
        media_type_id = int(request.form["media_type_id"])
        year = request.form["update_year"]

        edit_media_query = "UPDATE Media " \
                           "SET media_name=%s, media_type_id=%s, release_year=%s " \
                           "WHERE media_id=%s;"
        edit_media_query_params = (media_title, media_type_id, year, media_id)
        db_connection = db.connect_to_database()
        db.execute_query(db_connection,
                         edit_media_query, edit_media_query_params)
        db_connection.close()

        return redirect("/media")


@app.route('/delete_media/<int:id>', methods=["POST", "GET"])
def delete_media(id):
    # Display Are you sure you want to delete the media? page with record to
    # be deleted
    if request.method == "GET":
        media_query = "SELECT media_id, media_name from Media " \
                      "WHERE media_id=%s;"
        media_query_params = (id,)
        db_connection = db.connect_to_database()
        media_data = db.execute_query(
                db_connection,
                media_query,
                media_query_params).fetchall()
        db_connection.close()

        return render_template('delete_media.html', media_data=media_data)

    # Delete the planet
    if request.method == "POST":
        planet_id = int(request.form["media_id"])
        delete_media_query = "DELETE FROM Media WHERE media_id=%s;"
        delete_media_query_params = (planet_id,)
        db_connection = db.connect_to_database()
        db.execute_query(db_connection,
                         delete_media_query, delete_media_query_params)
        db_connection.close()

        return redirect("/media")


@app.route('/media_types', methods=["GET"])
def browse_media_types():
    # Get the data to display on the media types page
    media_types_query = "SELECT media_type_id AS 'ID', media_type AS 'Type' " \
                        "FROM Media_Types;"
    db_connection = db.connect_to_database()
    media_type_data = db.execute_query(db_connection,
                                       media_types_query).fetchall()
    db_connection.close()

    return render_template("media_types.html", media_types=media_type_data)


@app.route('/regions', methods=["POST", "GET"])
def browse_regions():
    # Page for browsing all regions
    regions_query = "SELECT region_id AS 'ID', region_name AS 'Region' " \
                    "FROM Regions;"
    db_connection = db.connect_to_database()
    regions_data = db.execute_query(db_connection, regions_query).fetchall()
    db_connection.close()

    return render_template("regions.html", regions=regions_data)


@app.route('/species', methods=["POST", "GET"])
def browse_species():
    # Page for browsing all species
    if request.method == 'GET':
        species_query = "SELECT species_id AS 'ID', " \
                        "classification AS 'Species Classification', " \
                        "Planets.planet_name AS 'Species Planet of Origin' " \
                        "FROM Species LEFT JOIN Planets " \
                        "ON species_home_planet = Planets.planet_id;"
        db_connection = db.connect_to_database()
        species_data = db.execute_query(db_connection,
                                        species_query).fetchall()
        db_connection.close()

        # planets drop-down data to be used on the add new species page
        planets_drop_down_query = "SELECT planet_id, planet_name FROM Planets;"
        db_connection = db.connect_to_database()
        planets_data = db.execute_query(db_connection,
                                        planets_drop_down_query).fetchall()
        db_connection.close()

        return render_template("species.html", species=species_data,
                               planets_dropdown=planets_data)

    # Add new species
    elif request.method == 'POST':
        species_home_planet = int(request.form['species_planet'])
        species_classification = request.form['species_classification']

        # Insert species with null home planet
        if species_home_planet == -1:
            insert_species_query = "INSERT INTO Species (classification) VALUES (%s);"
            insert_species_params = (species_classification,)
            db_connection = db.connect_to_database()
            db.execute_query(db_connection,
                             insert_species_query, insert_species_params)
            db_connection.close()

            return redirect('/species')

        # Insert new planet and new species
        elif species_home_planet == -2:
            regions_query = "SELECT region_id, region_name FROM Regions;"
            db_connection = db.connect_to_database()
            regions_data = db.execute_query(db_connection,
                                            regions_query).fetchall()
            db_connection.close()
            return redirect(url_for('add_planet_and_species',
                                    new_species_classification=species_classification,
                                    regions_data=regions_data))

        # insert regular species with not null home planet
        else:
            insert_species_query = "INSERT INTO Species " \
                                   "(classification, species_home_planet) " \
                                   "VALUES (%s, %s);"
            insert_species_params = (
                    species_classification, species_home_planet)
            db_connection = db.connect_to_database()
            db.execute_query(db_connection,
                             insert_species_query,
                             insert_species_params)
            db_connection.close()

            return redirect('/species')


@app.route('/add-planet-and-species', methods=['POST', 'GET'])
def add_planet_and_species():
    # insert new planet and new species
    if request.method == 'POST':
        species_classification = request.form['species_classification'].title()
        planet_name = request.form['planet_name'].title()
        planet_region_id = int(request.form['region'])
        planet_first_appearance = int(request.form['media_id'])

        if request.form["planet_description"]:
            planet_description = request.form["planet_description"]
        else:
            planet_description = ""

        # double-check the new planet isn't already in the db
        find_matching_planets_query = "SELECT planet_id, planet_name " \
                                      "FROM Planets WHERE planet_name=%s;"

        find_matching_planets_query_params = (planet_name,)
        db_connection = db.connect_to_database()
        matches = db.execute_query(db_connection,
                                   find_matching_planets_query,
                                   find_matching_planets_query_params).fetchall()
        db_connection.close()
        count_planet_matches = len(matches)

        # Insert planet if it is not already present and get its ID
        if count_planet_matches == 0:
            # First insert new planet
            if planet_first_appearance == -1:
                # Insert planet with null first appearnce
                insert_new_planet_query = "INSERT INTO Planets " \
                                          "(planet_name, region_id, description) " \
                                          "VALUES (%s, %s, %s);"
                insert_new_planet_query_params = (
                        planet_name,
                        planet_region_id,
                        planet_description)
                db_connection = db.connect_to_database()
                cursor = db.execute_query(db_connection,
                                          insert_new_planet_query,
                                          insert_new_planet_query_params)
                planet_id = cursor.lastrowid
                db_connection.close()

            else:
                # insert planet with first appearance
                insert_new_planet_query = "INSERT INTO Planets " \
                                          "(planet_name, region_id, description, " \
                                          "planet_first_appearance) " \
                                          "VALUES (%s, %s, %s, %s);"
                insert_new_planet_query_params = (
                        planet_name,
                        planet_region_id,
                        planet_description,
                        planet_first_appearance)
                db_connection = db.connect_to_database()
                cursor = db.execute_query(db_connection,
                                          insert_new_planet_query,
                                          insert_new_planet_query_params)
                planet_id = cursor.lastrowid
                db_connection.close()

        # planet already exists, use existing planet_id
        else:
            planet_id = int(matches[0]['planet_id'])

        # Then insert new species
        if planet_id == -1:
            # insert new species with null home planet
            insert_new_species_query = "INSERT INTO Species (" \
                                       "classification) " \
                                       "VALUES (%s);"
            insert_new_species_query_params = (species_classification,)
        else:
            # insert species with planet
            insert_new_species_query = "INSERT INTO Species (" \
                                       "classification, " \
                                       "species_home_planet) " \
                                       "VALUES (%s, %s);"
            insert_new_species_query_params = (
                    species_classification, planet_id)
        db_connection = db.connect_to_database()
        db.execute_query(db_connection,
                         insert_new_species_query,
                         insert_new_species_query_params)
        db_connection.close()

        return redirect('/species')

    # Display insert form
    elif request.method == 'GET':
        first_appearances = "SELECT media_id, media_name FROM Media;"
        db_connection = db.connect_to_database()
        first_appearances_data = db.execute_query(db_connection,
                                                  first_appearances).fetchall()
        db_connection.close()

        regions_query = "SELECT region_id, region_name FROM Regions;"
        db_connection = db.connect_to_database()
        regions_data = db.execute_query(db_connection,
                                        regions_query).fetchall()
        db_connection.close()

        species_classification = request.args.get("new_species_classification")

        return render_template('add_planet_and_species.html',
                               media=first_appearances_data,
                               regions_data=regions_data,
                               new_species_classification=species_classification)


@app.route('/delete_species/<int:id>', methods=['POST', 'GET'])
def delete_species(id):
    # Display Are you sure you want to delete the species? page with record to
    # be deleted
    if request.method == "GET":
        species_query = "SELECT species_id, classification, " \
                        "Planets.planet_name " \
                        "FROM Species LEFT JOIN Planets " \
                        "ON species_home_planet = Planets.planet_id WHERE species_id=%s;"
        species_query_params = (id,)
        db_connection = db.connect_to_database()
        species_data = db.execute_query(
                db_connection,
                species_query,
                species_query_params).fetchall()
        db_connection.close()

        return render_template('delete_species.html',
                               species_data=species_data)

    # Delete the planet
    if request.method == "POST":
        species_id = int(request.form["species_id"])
        delete_species_query = "DELETE FROM Species WHERE species_id=%s;"
        delete_species_query_params = (species_id,)
        db_connection = db.connect_to_database()
        db.execute_query(db_connection,
                         delete_species_query, delete_species_query_params)
        db_connection.close()

        return redirect("/species")


@app.route('/edit_species/<int:id>', methods=['POST', 'GET'])
def edit_species(id):
    # Display the species entry to edit
    if request.method == "GET":
        species_query = "SELECT species_id AS 'ID', " \
                        "species_home_planet, " \
                        "classification AS 'Species Classification', " \
                        "Planets.planet_name AS 'Species Planet of Origin' " \
                        "FROM Species LEFT JOIN Planets " \
                        "ON species_home_planet = Planets.planet_id WHERE species_id=%s;"
        species_query_params = (id,)
        db_connection = db.connect_to_database()
        species_data = db.execute_query(db_connection,
                                        species_query,
                                        species_query_params).fetchall()
        db_connection.close()

        # planets drop-down menu data
        planets_drop_down_query = "SELECT planet_id, planet_name FROM Planets;"
        db_connection = db.connect_to_database()
        planets_data = db.execute_query(db_connection,
                                        planets_drop_down_query).fetchall()
        db_connection.close()

        return render_template('edit_species.html', species_data=species_data,
                               planets=planets_data)
    # Update the media entry in the DB
    if request.method == "POST":
        species_id = int(request.form['species_id'])
        species_classification = request.form["species_classification"]
        species_planet_id = int(request.form['planet_id'])

        # update species with null home planet
        if species_planet_id == -1:
            edit_species_query = "UPDATE Species SET classification=%s, species_home_planet=NULL WHERE species_id=%s;"
            edit_species_query_params = (
                    species_classification, species_id)
        # update species with non-null home planet
        else:
            edit_species_query = "UPDATE Species SET classification=%s, species_home_planet=%s WHERE species_id=%s;"
            edit_species_query_params = (
                    species_classification, species_planet_id, species_id)
        db_connection = db.connect_to_database()
        db.execute_query(db_connection,
                         edit_species_query, edit_species_query_params)
        db_connection.close()

        return redirect("/species")


@app.route('/characters', methods=["POST", "GET"])
# Get all Characters for browse page. Get Planet, Media, and Species for insert dropdowns.
def browse_characters():
    if request.method == 'GET':
        characters_query = "SELECT character_id AS 'Character ID', character_name AS 'Character Name', " \
                           "Planets.planet_name AS 'Character Home Planet', " \
                           "Media.media_name AS 'First Media Appearance', " \
                           "Species.classification AS 'Character Species', " \
                           "birth_year AS 'Birth Year' FROM Characters " \
                           "LEFT JOIN Planets " \
                           "ON character_home_planet = Planets.planet_id " \
                           "LEFT JOIN Species " \
                           "ON species = Species.species_id " \
                           "LEFT JOIN Media " \
                           "ON character_first_appearance = Media.media_id;"
        db_connection = db.connect_to_database()
        character_data = db.execute_query(db_connection,
                                          characters_query).fetchall()
        db_connection.close()
        # Get Planet, Media, and Species for insert dropdowns
        planet_query = "SELECT planet_id, planet_name FROM Planets;"
        db_connection = db.connect_to_database()
        planet_data = db.execute_query(db_connection, planet_query).fetchall()
        db_connection.close()

        media_query = "SELECT media_id, media_name FROM Media;"
        db_connection = db.connect_to_database()
        media_data = db.execute_query(db_connection,
                                      media_query).fetchall()
        db_connection.close()

        species_query = "SELECT species_id, classification FROM Species;"
        db_connection = db.connect_to_database()
        species_data = db.execute_query(db_connection,
                                        species_query).fetchall()
        db_connection.close()

        return render_template("characters.html",
                               character_data=character_data, planet_data=planet_data,
                                media_data=media_data, species_data=species_data)
    # Insert new Character with data from request form
    if request.method == 'POST':
        character_name = request.form["character_name"]
        character_home_planet = int(request.form["character_home_planet"])
        character_first_appearance = int(request.form["character_first_appearance"])
        character_species = int(request.form["character_species"])
        character_birth = request.form["character_birth_year"]
        
        # Build query and params based on which Nullable values are given with form
        character_query = "INSERT INTO Characters (character_name, "
        values = "VALUES (%s, "
        query_params = (character_name, )

        if character_home_planet != -1:
            character_query += "character_home_planet, "
            query_params += (character_home_planet, )
            values += "%s, "

        if character_first_appearance != -1:
            character_query += "character_first_appearance, "
            query_params += (character_first_appearance, )
            values += "%s, "

        character_query += "species"
        query_params += (character_species, )
        values += "%s"

        if character_birth != '':
            character_query += ", birth_year) "
            query_params += (character_birth, )
            values += ", %s)"
            character_query += values
        else:
            values += ")"
            character_query += ") "
            character_query += values

        db_connection = db.connect_to_database()
        db.execute_query(db_connection,
                        character_query, query_params)
        db_connection.close()

        return redirect("/characters")


@app.route("/edit_character/<int:id>", methods=["POST", "GET"])
# Get Character to edit with passed id. Get Planet, Media, and Species for insert dropdowns 
def edit_character(id):
    if request.method == 'GET':
        characters_query = "SELECT character_id, character_name, " \
                           "Planets.planet_name, " \
                           "Media.media_name, " \
                           "Species.classification, " \
                           "birth_year AS 'Birth Year' FROM Characters " \
                           "LEFT JOIN Planets " \
                           "ON character_home_planet = Planets.planet_id " \
                           "LEFT JOIN Species " \
                           "ON species = Species.species_id " \
                           "LEFT JOIN Media " \
                           "ON character_first_appearance = Media.media_id " \
                           "WHERE character_id = %s;"
        characters_query_params = (id,)
        db_connection = db.connect_to_database()
        character_data = db.execute_query(
                db_connection,
                characters_query,
                characters_query_params).fetchall()
        db_connection.close()
        # Get Planet, Media, and Species for insert dropdowns
        planet_query = "SELECT planet_id, planet_name FROM Planets;"
        db_connection = db.connect_to_database()
        planet_data_dropdown = db.execute_query(db_connection,
                                                planet_query).fetchall()
        db_connection.close()

        media_query = "SELECT media_id, media_name FROM Media;"
        db_connection = db.connect_to_database()
        media_data_dropdown = db.execute_query(db_connection,
                                               media_query).fetchall()
        db_connection.close()

        species_query = "SELECT species_id, classification FROM Species;"
        db_connection = db.connect_to_database()
        species_data_dropdown = db.execute_query(db_connection,
                                                 species_query).fetchall()
        db_connection.close()

        return render_template("edit_character.html", character_data=character_data, planet_data_dropdown=planet_data_dropdown,
                                media_data_dropdown=media_data_dropdown, species_data_dropdown=species_data_dropdown)
    # Update Character in database with data from request form
    if request.method == 'POST':
        character_name = request.form["character_name"]
        character_home_planet = int(request.form["character_home_planet"])
        character_first_appearance = int(request.form["character_first_appearance"])
        character_species = int(request.form["character_species"])
        character_birth = request.form["character_birth_year"]

        # Build query and params based on which Nullable values are given with form
        character_query = "UPDATE Characters SET character_name = %s, "
        query_params = (character_name, )
        if character_home_planet != -1:
            character_query += "character_home_planet = %s, "
            query_params += (character_home_planet, )
        else:
            character_query += "character_home_planet = NULL, "

        if character_first_appearance != -1:
            character_query += "character_first_appearance = %s, "
            query_params += (character_first_appearance, )
        else:
            character_query += "character_first_appearance = NULL, "

        character_query += "species  = %s"
        query_params += (character_species, )
        if character_birth != '':
            character_query += ", birth_year = %s "
            query_params += (character_birth, )
        else:
            character_query += ", birth_year = NULL "

        
        character_query += "WHERE character_id = %s;"
        query_params += (id, )

        db_connection = db.connect_to_database()
        db.execute_query(db_connection,
                        character_query, query_params)
        db_connection.close()

        return redirect("/characters")


@app.route("/delete_character/<int:id>", methods=["POST", "GET"])
# Get Character with passed id to confirm delete request
def delete_character(id):
    if request.method == 'GET':
        query = "SELECT character_id AS 'Character ID', character_name AS 'Character Name', " \
                "Planets.planet_name AS 'Character Home Planet', " \
                "Media.media_name AS 'First Media Appearance', " \
                "Species.classification AS 'Character Species', " \
                "birth_year AS 'Birth Year' FROM Characters " \
                "LEFT JOIN Planets " \
                "ON character_home_planet = Planets.planet_id " \
                "LEFT JOIN Species " \
                "ON species = Species.species_id " \
                "LEFT JOIN Media " \
                "ON character_first_appearance = Media.media_id WHERE character_id = %s;"

        db_connection = db.connect_to_database()
        character_data = db.execute_query(db_connection,
                                          query, (id,)).fetchall()
        db_connection.close()

        return render_template("delete_character.html", character_data=character_data)
    # Delete character from database with passed id
    if request.method == 'POST':
        query = "DELETE FROM Characters WHERE character_id = '%s';"

        db_connection = db.connect_to_database()
        db.execute_query(db_connection,
                         query, (id,))
        db_connection.close()

        return redirect("/characters")


@app.route('/character_affiliations', methods=["POST", "GET"])
# Get Character Affiliations. Get Characters and Affiliations for insert dropdowns. 
def browse_character_affiliations():
    if request.method == 'GET':
        character_query = "SELECT Characters.character_name AS 'Character Name', Characters.character_id AS 'Character ID'," \
             "Affiliations.affiliation AS 'Affiliation Name', Affiliations.affiliation_id AS 'Affiliation ID' FROM Characters " \
                "JOIN Character_Affiliations ON Character_Affiliations.character_id = Characters.character_id JOIN Affiliations " \
                    "ON Affiliations.affiliation_id = Character_Affiliations.affiliation_id;"
        db_connection = db.connect_to_database()
        affiliation_data = db.execute_query(db_connection,
                                            character_query).fetchall()
        db_connection.close()
        # Get Characters and Affiliations for insert dropdowns.
        characters_query = "SELECT character_id, character_name FROM Characters;"
        db_connection = db.connect_to_database()
        characters_dropdown = db.execute_query(db_connection,
                                               characters_query).fetchall()
        db_connection.close()

        affiliation_query = "SELECT affiliation_id, affiliation FROM Affiliations;"
        db_connection = db.connect_to_database()
        affilations_data_dropdown = db.execute_query(db_connection,
                                                     affiliation_query).fetchall()
        db_connection.close()

        return render_template("character_affiliations.html",
                               affiliation_data=affiliation_data, characters_dropdown=characters_dropdown, affilations_data_dropdown=affilations_data_dropdown)
    # Insert new Character Affiliation with data from request form
    if request.method == 'POST':
        character_id = int(request.form["character_name"])
        affilation_id = int(request.form["affiliaton_name"])

        characters_query = "SELECT Characters.character_name AS 'Character Name', Characters.character_id AS 'Character ID'," \
             "Affiliations.affiliation AS 'Affiliation Name', Affiliations.affiliation_id AS 'Affiliation ID' FROM Characters " \
                "JOIN Character_Affiliations ON Character_Affiliations.character_id = Characters.character_id JOIN Affiliations " \
                    "ON Affiliations.affiliation_id = Character_Affiliations.affiliation_id;"

        db_connection = db.connect_to_database()
        character_ship_data = db.execute_query(db_connection,
                                               characters_query).fetchall()
        db_connection.close()

        for item in character_ship_data:
            if item['Character ID'] == character_id and item['Affiliation ID'] == affilation_id:
                flash("Unable to add because of an existing table entry")
                return redirect("/character_affiliations")

        query = "INSERT INTO Character_Affiliations (character_id, affiliation_id)" \
                "VALUES (%s, %s)"

        db_connection = db.connect_to_database()
        db.execute_query(db_connection,
                         query, (character_id, affilation_id))
        db_connection.close()

        return redirect("/character_affiliations")

@app.route('/delete_character_affiliation/<int:character_id>/<int:affiliation_id>', methods=["POST", "GET"])
# Get Character Affiliation with passed ids to confirm delete request
def delete_character_affiliation(character_id, affiliation_id):
    if request.method == 'GET':
        characters_query = "SELECT Characters.character_name AS 'Character Name', Characters.character_id, " \
                           "Affiliations.affiliation_id, Affiliations.affiliation AS 'Affiliation Name' " \
                           "FROM Characters " \
                           "JOIN Character_Affiliations " \
                           "ON Character_Affiliations.character_id = Characters.character_id " \
                           "JOIN Affiliations ON Affiliations.affiliation_id = " \
                           "Character_Affiliations.affiliation_id " \
                           "WHERE Characters.character_id = %s AND Affiliations.affiliation_id = %s;"
        db_connection = db.connect_to_database()
        character_data = db.execute_query(db_connection, characters_query, (
                character_id, affiliation_id,)).fetchall()
        db_connection.close()
        return render_template("delete_character_affiliation.html",
                               character_data=character_data)
    # Delete Character Affiliation from database
    if request.method == 'POST':
        delete_query = "DELETE FROM Character_Affiliations WHERE character_id = '%s' AND affiliation_id = '%s';"

        db_connection = db.connect_to_database()
        db.execute_query(db_connection,
                         delete_query, (character_id, affiliation_id,))
        db_connection.close()

        return redirect("/character_affiliations")

@app.route("/edit_character_affiliation/<int:character_id>/<int:affiliation_id>", methods=["POST", "GET"])
# Get Character Affiliation to edit with passed ids. Get Characters and Affiliations for insert dropdowns 
def edit_character_affiliation(character_id, affiliation_id):
    if request.method == 'GET':
        characters_query = "SELECT Characters.character_name AS 'Character Name', Characters.character_id, " \
                           "Affiliations.affiliation_id, Affiliations.affiliation AS 'Affiliation Name' " \
                           "FROM Characters " \
                           "JOIN Character_Affiliations " \
                           "ON Character_Affiliations.character_id = Characters.character_id " \
                           "JOIN Affiliations ON Affiliations.affiliation_id = " \
                           "Character_Affiliations.affiliation_id " \
                           "WHERE Characters.character_id = %s AND Affiliations.affiliation_id = %s;"
        db_connection = db.connect_to_database()
        character_data = db.execute_query(db_connection,
                                          characters_query, (character_id,
                                                             affiliation_id,)).fetchall()
        db_connection.close()

        character_query = "SELECT character_id, character_name FROM Characters;"
        db_connection = db.connect_to_database()
        character_data_dropdown = db.execute_query(db_connection,
                                                   character_query).fetchall()
        db_connection.close()

        affiliation_query = "SELECT affiliation_id, affiliation FROM Affiliations;"
        db_connection = db.connect_to_database()
        affiliation_data_dropdown = db.execute_query(db_connection,
                                                     affiliation_query).fetchall()
        db_connection.close()

        return render_template("edit_character_affiliation.html", character_data=character_data, character_data_dropdown=character_data_dropdown,
                                affiliation_data_dropdown=affiliation_data_dropdown)
    # Update Character Affiliation in database with data from request form 
    if request.method == 'POST':
        new_character_id = int(request.form["new_character_id"])
        new_affiliation_id = int(request.form["new_affiliation_id"])
        old_character_id = int(request.form["old_character_id"])
        old_affiliation_id = int(request.form["old_affiliation_id"])

        characters_query = "SELECT Characters.character_name AS 'Character Name', Characters.character_id AS 'Character ID'," \
             "Affiliations.affiliation AS 'Affiliation Name', Affiliations.affiliation_id AS 'Affiliation ID' FROM Characters " \
                "JOIN Character_Affiliations ON Character_Affiliations.character_id = Characters.character_id JOIN Affiliations " \
                    "ON Affiliations.affiliation_id = Character_Affiliations.affiliation_id;"

        db_connection = db.connect_to_database()
        character_ship_data = db.execute_query(db_connection,
                                               characters_query).fetchall()
        db_connection.close()

        for item in character_ship_data:
            if item['Character ID'] == new_character_id and item['Affiliation ID'] == new_affiliation_id:
                flash("Unable to edit because of an existing table entry")
                return redirect("/character_affiliations")  

        update_query = "UPDATE Character_Affiliations SET character_id = %s, affiliation_id = %s WHERE character_id = %s AND affiliation_id = %s;"

        db_connection = db.connect_to_database()
        db.execute_query(db_connection,
                         update_query, (new_character_id, new_affiliation_id,
                                 old_character_id, old_affiliation_id))
        db_connection.close()
        return redirect("/character_affiliations")


@app.route('/affiliations', methods=["POST", "GET"])
# Get all Affiliations from database
def browse_affiliations():
    if request.method == 'GET':
        query = "SELECT affiliation_id AS 'ID', " \
                "affiliation AS 'Affiliation' " \
                "FROM Affiliations;"

        db_connection = db.connect_to_database()
        affiliation_data = db.execute_query(db_connection, query).fetchall()
        db_connection.close()

        return render_template("affiliations.html",
                               affiliation_data=affiliation_data)


@app.route('/ships', methods=["POST", "GET"])
# Get all Ships for browse page. Get Ship Classifications for insert dropdowns.
def browse_ships():
    if request.method == 'GET':
        query = "SELECT ship_id AS 'Ship ID', ship_name AS 'Ship Name', " \
                "Ship_Classifications.ship_type AS 'Ship Classification' " \
                "FROM Ships JOIN Ship_Classifications ON Ships.ship_type = " \
                "Ship_Classifications.ship_classification_id;"

        db_connection = db.connect_to_database()
        ship_data = db.execute_query(db_connection, query).fetchall()
        db_connection.close()

        query = "SELECT ship_classification_id, ship_type AS 'Ship Classification' FROM Ship_Classifications;"

        db_connection = db.connect_to_database()
        ship_types = db.execute_query(db_connection, query).fetchall()
        db_connection.close()

        return render_template("ships.html", ship_data=ship_data,
                               ship_types=ship_types)
    # Insert new Ship with data from request form 
    if request.method == 'POST':
        ship_name = request.form["ship_name"]
        ship_type = request.form["ship_type"]
        query = "INSERT INTO Ships (ship_name, ship_type) VALUES (%s, %s)"

        db_connection = db.connect_to_database()
        db.execute_query(db_connection, query, (ship_name, ship_type))
        db_connection.close()

        return redirect("/ships")


@app.route("/delete_ship/<int:id>", methods=["POST", "GET"])
# Get Ship from database to confirm delete request
def delete_ship(id):
    if request.method == 'GET':
        query = "SELECT ship_id AS 'Ship ID', ship_name AS 'Ship Name', " \
                "Ship_Classifications.ship_type AS 'Ship Classification' " \
                "FROM Ships JOIN Ship_Classifications ON Ships.ship_type = " \
                "Ship_Classifications.ship_classification_id WHERE ship_id = %s;"

        db_connection = db.connect_to_database()
        ship_data = db.execute_query(db_connection,
                                     query, (id,)).fetchall()
        db_connection.close()

        return render_template("delete_ship.html", ship_data=ship_data)
    # Delete Ship from databasea
    if request.method == 'POST':
        query = "DELETE FROM Ships WHERE ship_id = '%s';"

        db_connection = db.connect_to_database()
        db.execute_query(db_connection,
                         query, (id,))
        db_connection.close()

        return redirect("/ships")


@app.route("/edit_ship/<int:id>", methods=["POST", "GET"])
# Get Ship to edit with passed id. Get Ship Classification for insert dropdowns 
def edit_ships(id):
    if request.method == 'GET':
        query = "SELECT ship_id AS 'Ship ID', ship_name AS 'Ship Name', " \
                "Ship_Classifications.ship_type AS 'Ship Classification' " \
                "FROM Ships JOIN Ship_Classifications ON Ships.ship_type = " \
                "Ship_Classifications.ship_classification_id WHERE ship_id = %s;"
        db_connection = db.connect_to_database()
        ship_data = db.execute_query(db_connection, query, (id,)).fetchall()
        db_connection.close()

        query = "SELECT ship_classification_id, ship_type AS 'Ship Classification' FROM Ship_Classifications;"
        db_connection = db.connect_to_database()
        ship_types = db.execute_query(db_connection, query).fetchall()
        db_connection.close()

        return render_template("edit_ship.html", ship_data=ship_data,
                               ship_types=ship_types)
    # Update Ship with data from request form
    if request.method == 'POST':
        ship_name = request.form["ship_name"]
        ship_type = request.form["ship_type"]
        query = "UPDATE Ships SET ship_name = %s, ship_type = %s WHERE ship_id = %s;"
        db_connection = db.connect_to_database()
        db.execute_query(db_connection,
                         query, (ship_name, ship_type, id,))
        db_connection.close()

        return redirect("/ships")


@app.route('/character_ships', methods=["POST", "GET"])
# Get all Character Ships from database. Get Characters and Ships for dropdowns
def browse_character_ships():
    if request.method == 'GET':
        characters_query = "SELECT Characters.character_name AS 'Character Name', Characters.character_id AS 'Character ID', " \
                           "Ships.ship_name AS 'Ship Name', Ships.ship_id AS 'Ship ID' FROM Characters JOIN Character_Ships ON " \
                           "Character_Ships.character_id = Characters.character_id JOIN Ships ON Ships.ship_id = " \
                           "Character_Ships.ship_id;"

        db_connection = db.connect_to_database()
        character_ship_data = db.execute_query(db_connection,
                                               characters_query).fetchall()
        db_connection.close()
        # Get Characters and Ships for dropdowns
        characters_query = "SELECT character_id, character_name FROM Characters;"
        db_connection = db.connect_to_database()
        characters_dropdown = db.execute_query(db_connection,
                                               characters_query).fetchall()
        db_connection.close()

        ship_query = "SELECT ship_id, ship_name FROM Ships;"
        db_connection = db.connect_to_database()
        ships_data_dropdown = db.execute_query(db_connection,
                                               ship_query).fetchall()
        db_connection.close()

        return render_template("character_ships.html",
                               character_ship_data=character_ship_data, characters_dropdown=characters_dropdown, ships_data_dropdown=ships_data_dropdown)
    # Insert new Character Ship with data from request form
    if request.method == 'POST':
        character_id = int(request.form["character_name"])
        ship_id = int(request.form["ship_name"])

        characters_query = "SELECT Characters.character_name AS 'Character Name', Characters.character_id AS 'Character ID', " \
                           "Ships.ship_name AS 'Ship Name', Ships.ship_id AS 'Ship ID' FROM Characters JOIN Character_Ships ON " \
                           "Character_Ships.character_id = Characters.character_id JOIN Ships ON Ships.ship_id = " \
                           "Character_Ships.ship_id;"

        db_connection = db.connect_to_database()
        character_ship_data = db.execute_query(db_connection,
                                               characters_query).fetchall()
        db_connection.close()

        for item in character_ship_data:
            if item['Character ID'] == character_id and item['Ship ID'] == ship_id:
                flash("Unable to add because of an existing table entry")
                return redirect("/character_ships")

        query = "INSERT INTO Character_Ships (character_id, ship_id)" \
                "VALUES (%s, %s)"

        db_connection = db.connect_to_database()
        db.execute_query(db_connection, query, (character_id, ship_id))
        db_connection.close()

        return redirect("/character_ships")

@app.route('/delete_character_ship/<int:character_id>/<int:ship_id>', methods=["POST", "GET"])
# Get Character Ship from database to confirm delete request
def delete_character_ship(character_id, ship_id):
    if request.method == 'GET':
        characters_query = "SELECT Characters.character_name AS 'Character Name', Characters.character_id, " \
                           "Ships.ship_id, Ships.ship_name AS 'Ship Name' " \
                           "FROM Characters " \
                           "JOIN Character_Ships " \
                           "ON Character_Ships.character_id = Characters.character_id " \
                           "JOIN Ships ON Ships.ship_id = " \
                           "Character_Ships.ship_id " \
                           "WHERE Characters.character_id = %s AND Ships.ship_id = %s;"
        db_connection = db.connect_to_database()
        character_data = db.execute_query(db_connection, characters_query,
                                          (character_id, ship_id,)).fetchall()
        db_connection.close()
        return render_template("delete_character_ship.html",
                               character_data=character_data)
    # Delete Character Ship from database
    if request.method == 'POST':
        query = "DELETE FROM Character_Ships WHERE character_id = '%s' AND ship_id = '%s';"

        db_connection = db.connect_to_database()
        db.execute_query(db_connection,
                         query, (character_id, ship_id,))
        db_connection.close()

        return redirect("/character_ships")

@app.route("/edit_character_ship/<int:character_id>/<int:ship_id>", methods=["POST", "GET"])
# Get Character Ship with passed ids. Get Characters and Ships for insert dropdowns
def edit_character_ship(character_id, ship_id):
    if request.method == 'GET':
        characters_query = "SELECT Characters.character_name AS 'Character Name', Characters.character_id, " \
                           "Ships.ship_id, Ships.ship_name AS 'Ship Name' " \
                           "FROM Characters " \
                           "JOIN Character_Ships " \
                           "ON Character_Ships.character_id = Characters.character_id " \
                           "JOIN Ships ON Ships.ship_id = " \
                           "Character_Ships.ship_id " \
                           "WHERE Characters.character_id = %s AND Ships.ship_id = %s;"
        db_connection = db.connect_to_database()
        character_data = db.execute_query(db_connection,
                                          characters_query,
                                          (character_id, ship_id,)).fetchall()
        db_connection.close()

        character_query = "SELECT character_id, character_name FROM Characters;"
        db_connection = db.connect_to_database()
        character_data_dropdown = db.execute_query(db_connection,
                                                   character_query).fetchall()
        db_connection.close()

        ship_query = "SELECT ship_id, ship_name FROM Ships;"
        db_connection = db.connect_to_database()
        ship_data_dropdown = db.execute_query(db_connection,
                                              ship_query).fetchall()
        db_connection.close()

        return render_template("edit_character_ship.html", character_data=character_data, character_data_dropdown=character_data_dropdown,
                                ship_data_dropdown=ship_data_dropdown)
    # Update Character Ship with data from request form 
    if request.method == 'POST':
        new_character_id = int(request.form["new_character_id"])
        new_ship_id = int(request.form["new_ship_id"])
        old_character_id = int(request.form["old_character_id"])
        old_ship_id = int(request.form["old_ship_id"])

        characters_query = "SELECT Characters.character_name AS 'Character Name', Characters.character_id AS 'Character ID', " \
                           "Ships.ship_name AS 'Ship Name', Ships.ship_id AS 'Ship ID' FROM Characters JOIN Character_Ships ON " \
                           "Character_Ships.character_id = Characters.character_id JOIN Ships ON Ships.ship_id = " \
                           "Character_Ships.ship_id;"

        db_connection = db.connect_to_database()
        character_ship_data = db.execute_query(db_connection,
                                               characters_query).fetchall()
        db_connection.close()

        for item in character_ship_data:
            if item['Character ID'] == new_character_id and item['Ship ID'] == new_ship_id:
                flash("Unable to edit because of an existing table entry")
                return redirect("/character_ships")

        query = "UPDATE Character_Ships SET character_id = %s, ship_id = %s WHERE character_id = %s AND ship_id = %s;"

        db_connection = db.connect_to_database()
        db.execute_query(db_connection,
                         query, (
                                 new_character_id, new_ship_id,
                                 old_character_id,
                                 old_ship_id))
        db_connection.close()
        return redirect("/character_ships")

@app.route('/ship_classifications', methods=["POST", "GET"])
# Get all Ship Classifications from database
def browse_ships_classifications():
    if request.method == 'GET':
        query = "SELECT ship_classification_id AS 'Ship Classification ID', ship_type AS 'Ship Classification' FROM Ship_Classifications;"
        db_connection = db.connect_to_database()
        ship_data = db.execute_query(db_connection, query).fetchall()
        db_connection.close()

        return render_template("ship_classifications.html",
                               ship_data=ship_data)


# Listener

if __name__ == "__main__":
    app.run(port=31225, debug=True)

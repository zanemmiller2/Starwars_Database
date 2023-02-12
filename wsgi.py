from app import *
from templates import *
from static import *

from database import *
from flask import Flask, render_template, json, request
from flask_navigation import Navigation
import os

import database.db_connector as db

if __name__ == "__main__":
    app.run()

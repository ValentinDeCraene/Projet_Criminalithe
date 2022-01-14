from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from .constantes import SECRET_KEY

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")
statics = os.path.join(chemin_actuel, "static")

app = Flask(
    "Application",
    template_folder=templates,
    static_folder=statics
)
# On configure la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./bdd.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = SECRET_KEY
# On initie l'extension
db = SQLAlchemy(app)
login = LoginManager(app)

from .routes import accueil, index, index_amendes, amende, personne, source, index_personnes, index_sources
from flask import url_for
import datetime

from .. app import db

class Source(db.Model):
    source_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    source_date = db.Column(db.Integer)
    authorships = db.relationship("Authorship", back_populates="source")



class Amendes(db.Model):
    amendes_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    amendes_source_id = db.Column(db.Integer)
    amendes_montant = db.Column(db.Text)
    amendes_type = db.Column(db.Text)
    amendes_franche_verite = db.Column(db.Text)
    amendes_transcription = db.Column(db.Text)
    authorships = db.relationship("Authorship", back_populates="amende")


class Personnes(db.Model):
    personnes_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    personnes_amendes_id = db.Column(db.Integer)
    personnes_nom = db.Column(db.Text)
    personnes_prenom = db.Column(db.Text)
    authorships = db.relationship("Authorship", back_populates="personne")

class Authorship(db.Model):
    __tablename__= "authorship"
    authorship_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_amendes_id = db.Column(db.Integer, db.ForeignKey("amendes.amendes_id"))
    authorship_user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    authorship_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    authorship_personnes_id = db.Column(db.Integer, db.ForeignKey("personnes.personnes_id"))
    authorship_source_id = db.Column(db.Integer, db.ForeignKey("source.source_id"))
    user = db.relationship("User", back_populates="authorships")
    amende = db.relationship("Amendes", back_populates="authorships")
    personne = db.relationship("Personnes", back_populates="authorships")
    source = db.relationship("Source", back_populates="authorships")
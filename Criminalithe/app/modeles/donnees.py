from .. app import db

class Source(db.Model):
    source_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    source_date = db.Column(db.Integer)

class Amendes(db.Model):
    amendes_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    amendes_source_id = db.Column(db.Integer)
    amendes_montant = db.Column(db.Text)
    amendes_type = db.Column(db.Text)
    amendes_franche_verite = db.Column(db.Text)
    amendes_transcription = db.Column(db.Text)

class Personnes(db.Model):
    personnes_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    personnes_amendes_id = db.Column(db.Integer)
    personnes_nom = db.Column(db.Text)
    personnes_prenom = db.Column(db.Text)
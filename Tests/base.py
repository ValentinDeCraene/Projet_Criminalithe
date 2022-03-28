from Criminalithe.app.app import db, config_app, login
from Criminalithe.app.modeles.utilisateurs import User
from Criminalithe.app.modeles.donnees import Personnes, Amendes, Source, Authorship
from unittest import TestCase

class Base(TestCase):
    names = [
        Personnes(
            personnes_id='200',
            personnes_amendes_id='200',
            personnes_nom='Jehan',
            personnes_prenom='Du Pont',
        )
    ]

    def setUp(self):
        self.app = config_app("test")
        self.db = db
        self.client = self.app.test_client()
        self.db.create_all(app=self.app)

    def tearDown(self):
        self.db.drop_all(app=self.app)

    def insert_all(self, names=True):
        # On donne à notre DB le contexte d'exécution
        with self.app.app_context():
            if names:
                for fixture in self.names:
                    self.db.session.add(fixture)
            self.db.session.commit()
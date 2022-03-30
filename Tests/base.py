from Criminalithe.app.app import db, config_app, login
from Criminalithe.app.modeles.utilisateurs import User
from Criminalithe.app.modeles.donnees import Personnes, Amendes, Source, Authorship
from unittest import TestCase

class Base(TestCase):
    personnes = [
        Personnes(
            personnes_id='200',
            personnes_amendes_id='200',
            personnes_nom='Jehan',
            personnes_prenom='Du Pont',
        ),
        Personnes(
            personnes_id='201',
            personnes_amendes_id='201',
            personnes_nom='Jacquemet',
            personnes_prenom='Le Noir',
        ),
        Personnes(
            personnes_id='202',
            personnes_amendes_id='202',
            personnes_nom='Henri',
            personnes_prenom='Le Mestre',
        ),
    ],
    amendes = [
        Amendes(
            amendes_id="200",
            amendes_source_id = "6245",
            amendes_montant = "60",
            amendes_type = "violence_physique",
            amendes_franche_verite = "non",
            amendes_transcription = "pour avoir manié et volenté ung denommé Jehan de la Salle es mettres dudit bailliage",
            amendes_personnes_id ="200"
        ),
        Amendes(
            amendes_id="201",
            amendes_source_id="6245",
            amendes_montant="40",
            amendes_type="defaut_entretien",
            amendes_franche_verite="non",
            amendes_transcription="pour ce qu'il avoit esté trouver ung default de resparacion de sien heritaige cis es village de Fretin",
            amendes_personnes_id="201"
        ),
        Amendes(
            amendes_id="202",
            amendes_source_id="6245",
            amendes_montant="80",
            amendes_type="port-armes",
            amendes_franche_verite="non",
            amendes_transcription="pour ce qu'il avoit esté trouver pourtant ung glaive es mettes dudit bailliage",
            amendes_personnes_id="202"
        ),
    ],
    sources = [
        Source(
            source_id="6245",
            source_date = "1445"
        ),
        Source(
            source_id="6246",
            source_date="1445"
        ),
        Source(
            source_id="6247",
            source_date="1446"
        )]

    def setUp(self):
        self.app = config_app("test")
        self.db = db
        self.client = self.app.test_client()
        self.db.create_all(app=self.app)

    def tearDown(self):
        self.db.drop_all(app=self.app)

    def insert_all(self, amendes=True):
        # On donne à notre DB le contexte d'exécution
        with self.app.app_context():
            if amendes:
                for fixture in self.amendes:
                    self.db.session.add(fixture)
            self.db.session.commit()
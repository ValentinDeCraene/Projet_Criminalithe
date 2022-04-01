from Criminalithe.app.app import db, config_app, login
from Criminalithe.app.modeles.donnees import Personnes, Amendes, Source
from unittest import TestCase

# Pour une raison que je ne suis pas parvenu à identifier, je n'arrive pas à lancer
# les tests avec la commande python -m unittest discover Tests. Cependant, en cliquant ci-dessous
# sur Run, le test semble se lancer.

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
            amendes_transcription = "pour ce qu'il avoit este pourtrais d'avoir manie es mettes dudit bailliage ung certain Jacques Le Blond",
            amendes_personnes_id ="200"
        ),
        Amendes(
            amendes_id="201",
            amendes_source_id="6245",
            amendes_montant="40",
            amendes_type="defaut_entretien",
            amendes_franche_verite="non",
            amendes_transcription="pour avoir fait default heritaige es mettes dudit bailliage",
            amendes_personnes_id="201"
        ),
        Amendes(
            amendes_id="202",
            amendes_source_id="6245",
            amendes_montant="80",
            amendes_type="port-armes",
            amendes_franche_verite="non",
            amendes_transcription="pourte armes nues deffendues",
            amendes_personnes_id="202"
        ),
    ],
    sources = [
        Source(
            source_id="6245",
            source_date="1445"
        ),
        Source(
            source_id="6246",
            source_date="1445"
        ),
        Source(
            source_id="6247",
            source_date="1446"
        ),
    ]

    def setUp(self):
        self.app = config_app("test")
        self.db = db
        self.client = self.app.test_client()
        self.db.create_all(app=self.app)

    def tearDown(self):
        self.db.drop_all(app=self.app)

    def insert_all(self, personnes=True, amendes=True, sources=True):
        with self.app.app_context():
            if amendes:
                for fixture in self.amendes:
                    self.db.session.add(fixture)
            if personnes:
                for fixture in self.personnes:
                    self.db.session.add(fixture)
            if sources:
                for fixture in self.sources:
                    self.db.session.add(fixture)
            self.db.session.commit()

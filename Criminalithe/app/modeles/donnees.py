from flask import url_for
# datetime permet de tracer l'historique des modifications
import datetime, jsonify, json
from sqlalchemy import and_
from ..app import db


# On a recours ici à un ORM pour créer nos classes:


class Source(db.Model):
    source_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    source_date = db.Column(db.Integer)
    authorships = db.relationship("Authorship", back_populates="source")
    amendes = db.relationship("Amendes", back_populates="source")

#Méthode statique qui permet d'ajouter une source à la BDD. Elle est appelée dans la route correspondante.

    @staticmethod
    def ajout_source(ajout_source_id, ajout_source_date):
        erreurs = []
        if not ajout_source_id:
            erreurs.append("Veuillez renseigner l'identifiant pour cette source.")
        if not ajout_source_date:
            erreurs.append(
                "Veuillez renseigner la date de cette source.")

            # S'il y a au moins une erreur, afficher un message d'erreur.
        if len(erreurs) > 0:
            return False, erreurs

            # Si aucune erreur n'a été détectée, ajout d'une nouvelle entrée dans la table Amendes (champs correspondant aux paramètres du modèle)
        nouvelle_source = Source(source_id=ajout_source_id,
                                 source_date=ajout_source_date)

        # Tentative d'ajout qui sera stoppée si une erreur apparaît en uilisant try et except
        # (On anticipe les erreurs en les ajoutants le cas échéant dans une liste vide, qui est transformée en chaîne de caractères)
        try:
            db.session.add(nouvelle_source)
            db.session.commit()
            return True, nouvelle_source

        except Exception as erreur:
            return False, [str(erreur)]


    @staticmethod
    #Méthode statique qui permet de supprimer une source et qui est appelée dans la route correspondante.

    def supprimer_source(source_id):

        suppr_source = Source.query.get(source_id)

        try:
            db.session.delete(suppr_source)
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]

    #Fonction qui permet de "transformer" les données issue de la table concernée en un dictionnaire,
    #qui est ensuite utilisé dans l'API pour retourner des données au format JSON.

    def source_to_jsonapi_dict(self):
        return {
            "type": "source",
            "id": self.source_id,
            "attributes": {
                "source_date": self.source_date
            },
            "links": {
                "self": url_for("source", source_id=self.source_id, _external=True),
                "json": url_for("api_source", source_id=self.source_id, _external=True)
            },
            "relationships": {
                "editions": [
                    author.author_to_json()
                    for author in self.authorships]
            }
        }


class Amendes(db.Model):
    amendes_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    amendes_source_id = db.Column(db.Integer, db.ForeignKey("source.source_id"))
    amendes_montant = db.Column(db.Integer)
    amendes_type = db.Column(db.Text)
    amendes_franche_verite = db.Column(db.Text)
    amendes_transcription = db.Column(db.Text)
    amendes_personnes_id = db.Column(db.Integer, db.ForeignKey("personnes.personnes_amendes_id"))
    authorships = db.relationship("Authorship", back_populates="amende")
    justiciable = db.relationship("Personnes", foreign_keys="Personnes.personnes_amendes_id", backref="justiciable")
    source = db.relationship("Source", back_populates="amendes")



    # Méthode statique qui permet d'ajouter une amende à la BDD. Elle est appelée dans la route correspondante.

    @staticmethod
    def ajout_amende(ajout_amendes_id, ajout_amendes_source_id, ajout_amendes_montant, ajout_amendes_type,
                     ajout_amendes_franche_verite,
                     ajout_amendes_transcription):
        erreurs = []
        if not ajout_amendes_id:
            erreurs.append("Veuillez renseigner l'id pour cette amendes.")
        if not ajout_amendes_source_id:
            erreurs.append(
                "Veuillez renseigner une l'id de la source pour cette amende.")
        if not ajout_amendes_montant:
            erreurs.append(
                "Veuillez renseigner le montant de cette amende (en sous parisis si possible.")
        if not ajout_amendes_type:
            erreurs.append(
                "Veuillez renseigner le type de l'amende")
        if not ajout_amendes_franche_verite:
            erreurs.append(
                "Veuillez renseigner si cette amende est issue d'une franche-vérité (oui/non)")
        if not ajout_amendes_transcription:
            erreurs.append(
                "Veuillez indiquer la transcription de cette amende.")

            # S'il y a au moins une erreur, afficher un message d'erreur.
        if len(erreurs) > 0:
            return False, erreurs

            # Si aucune erreur n'a été détectée, ajout d'une nouvelle entrée dans la table Amendes (champs correspondant aux paramètres du modèle)
        nouvelle_amende = Amendes(amendes_id=ajout_amendes_id,
                                  amendes_source_id=ajout_amendes_source_id,
                                  amendes_montant=ajout_amendes_montant,
                                  amendes_type=ajout_amendes_type,
                                  amendes_franche_verite=ajout_amendes_franche_verite,
                                  amendes_transcription=ajout_amendes_transcription)

        # Tentative d'ajout qui sera stoppée si une erreur apparaît.
        try:
            db.session.add(nouvelle_amende)
            db.session.commit()
            return True, nouvelle_amende

        except Exception as erreur:
            return False, [str(erreur)]

#Méthode statique qui permet de supprimer une amende et qui est appelée dans la route correspondante.

    @staticmethod
    def supprimer_amende(amendes_id):

        suppr_amende = Amendes.query.get(amendes_id)

        try:
            db.session.delete(suppr_amende)
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]


    # Fonction qui permet de "transformer" les données issue de la table concernée en un dictionnaire,
    # qui est ensuite utilisé dans l'API pour retourner des données au format JSON.

    def amendes_to_jsonapi_dict(self):
        return {
            "type": "amende",
            "id": self.amendes_id,
            "attributes": {
                "amendes_id": self.amendes_id,
                "amendes_source_id": self.amendes_source_id,
                "amendes_montant": self.amendes_montant,
                "amendes_type": self.amendes_type,
                "amendes_franche_verite": self.amendes_franche_verite,
                "amendes_transcription": self.amendes_transcription,
                "amendes_personnes_id": self.amendes_personnes_id
            },
            "links": {
                "justiciables(personnes)": url_for("api_personnes", personnes_id=self.amendes_personnes_id, _external=True),
                "self": url_for("amende", amendes_id=self.amendes_id, _external=True),
                "json": url_for("api_amendes", amendes_id=self.amendes_id, _external=True),
                "source": url_for("source", source_id=self.amendes_source_id, _external=True)

            },
            "relationships": {
                "editions": [
                    author.author_to_json()
                    for author in self.authorships
                ]
                # "justiciables": [
                #     justiciable.justiciables()
                #     for justiciable in self.justiciable
                # ]
            }
        }

class Personnes(db.Model):
    personnes_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    personnes_amendes_id = db.Column(db.Integer, db.ForeignKey("amendes.amendes_personnes_id"))
    personnes_nom = db.Column(db.Text)
    personnes_prenom = db.Column(db.Text)
    authorships = db.relationship("Authorship", back_populates="personne")
    amendes = db.relationship("Amendes", backref="amendes", foreign_keys="Amendes.amendes_personnes_id")


    # Méthode statique qui permet d'ajouter une personne à la BDD. Elle est appelée dans la route correspondante.

    @staticmethod
    def ajout_personne(ajout_personnes_id, ajout_personnes_amendes_id, ajout_personnes_nom, ajout_personnes_prenom):
        erreurs = []
        if not ajout_personnes_id:
            erreurs.append("Veuillez renseigner l'identifiant pour cette personne.")
        if not ajout_personnes_amendes_id:
            erreurs.append(
                "Veuillez renseigner l'identifiant de l'amende mentionnant cette amende.")
        if not ajout_personnes_nom:
            erreurs.append(
                "Veuillez renseigner le nom de cette personne")
        if not ajout_personnes_prenom:
            erreurs.append(
                "Veuillez renseigner le prénom de cette personne")

            # S'il y a au moins une erreur, afficher un message d'erreur.
        if len(erreurs) > 0:
            return False, erreurs

            # Si aucune erreur n'a été détectée, ajout d'une nouvelle entrée dans la table AMendes (champs correspondant aux paramètres du modèle)
        nouvelle_personne = Personnes(personnes_id=ajout_personnes_id,
                                      personnes_amendes_id=ajout_personnes_amendes_id,
                                      personnes_nom=ajout_personnes_nom,
                                      personnes_prenom=ajout_personnes_prenom)

        # Tentative d'ajout qui sera stoppée si une erreur apparaît.
        try:
            db.session.add(nouvelle_personne)
            db.session.commit()
            return True, nouvelle_personne

        except Exception as erreur:
            return False, [str(erreur)]


    #Méthode statique qui permet de supprimer une personne et qui est appelée dans la route correspondante.

    @staticmethod
    def supprimer_personne(personnes_id):

        suppr_personne = Personnes.query.get(personnes_id)

        try:
            db.session.delete(suppr_personne)
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]


    # Fonction qui permet de "transformer" les données issue de la table concernée en un dictionnaire,
    # qui est ensuite utilisé dans l'API pour retourner des données au format JSON.

    def personnes_to_jsonapi_dict(self):
        return {
            "type": "personnes",
            "id": self.personnes_id,
            "attributes": {
                "personnes_amendes_id": self.personnes_amendes_id,
                "personnes_nom": self.personnes_nom,
                "personnes_prenom": self.personnes_prenom
            },
            "links": {
                "self": url_for("personne", personnes_id=self.personnes_id, _external=True),
                "json": url_for("api_personnes", personnes_id=self.personnes_id, _external=True),
                "amende": url_for("api_amendes", amendes_id=self.personnes_amendes_id, _external=True)

            },
            "relationships": {
                "editions": [
                    author.author_to_json()
                    for author in self.authorships
                ]
            }
        }



class Authorship(db.Model):
    __tablename__ = "authorship"
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

    # Fonction qui permet de "transformer" les données issue de la table concernée en un dictionnaire,
    # qui est ensuite utilisé dans l'API pour retourner des données au format JSON.

    def author_to_json(self):
        return {
            "author": self.user.to_jsonapi_dict(),
            "on": self.authorship_date
        }

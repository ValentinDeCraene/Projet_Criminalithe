from flask import Flask, render_template, request
from sqlalchemy import and_, or_
from .app import app
from .modeles.donnees import Source, Amendes, Personnes
@app.route("/")
def accueil():
    return render_template("pages/accueil.html")

@app.route("/Index/")
def index():
    return render_template("pages/Index.html")

@app.route("/Index/amendes/")
def index_amendes():
    amendes = Amendes.query.all()
    return render_template("pages/Index_amendes.html", amendes=amendes)

@app.route("/amende/<int:amendes_id>")
def amende(amendes_id):
    amende_unique = Amendes.query.filter(Amendes.amendes_id==amendes_id).first()
    return render_template("pages/amende.html", amende=amende_unique)

@app.route("/personne/<int:personnes_id>")
def personne(personnes_id):
    personne_unique = Personnes.query.filter(Personnes.personnes_id==personnes_id).first()
    return render_template("pages/personne.html", personne=personne_unique)

@app.route("/source/<int:source_id>")
def source(source_id):
    source_unique = Source.query.filter(Source.source_id==source_id).first()
    return render_template("pages/source.html", source=source_unique)

@app.route("/Index/personnes/")
def index_personnes():
    personnes = Personnes.query.all()
    return render_template("pages/Index_personnes.html", personnes=personnes)

@app.route("/Index/sources/")
def index_sources():
    sources = Source.query.all()
    return render_template("pages/Index_sources.html", sources=sources)

@app.route("/recherche")
def recherche():
    motclef = request.args.get("keyword", None)
    resultats = []
    titre = "Recherche"
    if motclef:
        resultats =\
            Amendes.query.filter(or_(
                    Amendes.amendes_transcription.like("%{}%".format(motclef)),
                    Amendes.amendes_id.like("%{}%".format(motclef)),
                    Amendes.amendes_type.like("%{}%".format(motclef)),
                    Amendes.amendes_montant.like("%{}%".format(motclef)),
                    Amendes.amendes_source_id.like("%{}%".format(motclef)),
                    Amendes.amendes_franche_verite.like("%{}%".format(motclef))
                )
            ).all()
        titre = "Résultat pour la recherche `" + motclef + "`"
    return render_template("pages/recherche.html", resultats=resultats, titre=titre)

#Personnes.query.filter(or_(
        #Personnes.personnes_id.like("%{}%".format(motclef)),
        #Personnes.personnes_prenom.like("%{}%".format(motclef),
        #Personnes.personnes_nom.like("%{}%".format(motclef),
        #Personnes.personnes_amendes_id("%{}%".format(motclef)))))).all()
from flask import Flask, render_template, request
from .modeles.donnees import Source, Amendes, Personnes
from sqlalchemy import and_, or_
from .app import app
from .constantes import RESULTATS_PAR_PAGES

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
    page = request.args.get("page", 1)
    resultats = []
    titre = "Recherche"

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

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
            ).paginate(page=page, per_page=RESULTATS_PAR_PAGES)

        titre = "Résultat pour la recherche `" + motclef + "`"
    return render_template("pages/recherche.html", resultats=resultats, titre=titre, keyword=motclef)

#Une possibilité est la suivante :
#def recherche():
    #motclef = request.args.get("keyword", None)
    #resultats = []
    #titre = "Recherche"
    #if motclef:
        #resultatsAmendes =\
            #Amendes.query.filter(or_(
                    #Amendes.amendes_transcription.like("%{}%".format(motclef)),
                    #Amendes.amendes_id.like("%{}%".format(motclef)),
                    #Amendes.amendes_type.like("%{}%".format(motclef)),
                    #Amendes.amendes_montant.like("%{}%".format(motclef)),
                    #Amendes.amendes_source_id.like("%{}%".format(motclef)),
                    #Amendes.amendes_franche_verite.like("%{}%".format(motclef))
                #)
            #).all()
        #if resultatsAmendes:
            # Pour que resultats ne se transforme pas en liste de listes (chaque table interrogée rendant une liste),
            # boucler sur chaque résultat pour l'ajouter
            #for resultat in resultatsAmendes:
                #resultats.append(resultat)

        # Sur un attribut de la table Personnes
        #resultatsPersonnes = Personnes.query.filter(Personnes.personnes_nom.like("%{}%".format(motclef))).all()
        #if resultatsPersonnes:
            #for resultat in resultatsPersonnes:
                #resultats.append(resultat)

        #titre = "Résultat pour la recherche `" + motclef + "`"
    #return render_template("pages/recherche.html", resultats=resultats, titre=titre)


#Si j'ajoute les paramètres suivants, je me retrouve face à une erreur de type NotCallable
#De plus, problème avec la méthode paginate qui renvoie un objet non iteable donc impossible d'ajouter les deux résultats.
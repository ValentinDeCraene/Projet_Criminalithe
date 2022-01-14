from flask import Flask, render_template, request, flash, redirect
from .modeles.donnees import Source, Amendes, Personnes
from .modeles.utilisateurs import User
from sqlalchemy import and_, or_
from .app import app, login
from .constantes import RESULTATS_PAR_PAGES
from flask_login import login_user, current_user, logout_user

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

@app.route("/inscription", methods=["GET", "POST"])
def inscription():

    if request.method == "POST":
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")


@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """ Route gérant les connexions
    """
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté-e", "info")
        return redirect("/")
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        utilisateur = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect("/")
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")

    return render_template("pages/connexion.html")
login.login_view = 'connexion'


@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e", "info")
    return redirect("/")


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
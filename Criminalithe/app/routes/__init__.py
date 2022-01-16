from flask import Flask, render_template, request, flash, redirect

from ..app import app, login, db
from ..modeles.donnees import Source, Amendes, Personnes, Authorship
from ..modeles.utilisateurs import User
from sqlalchemy import and_, or_
from ..constantes import RESULTATS_PAR_PAGES
from flask_login import login_user, current_user, logout_user, login_required

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


@app.route("/personne/<int:personnes_id>/update", methods=["GET", "POST"])
@login_required
def personne_update(personnes_id):

    ma_personne = Personnes.query.get(personnes_id)

    erreurs = []
    updated = False

    if request.method == "POST":
        # J"ai un formulaire
        if not request.form.get("personnes_id", "").strip():
            erreurs.append("personnes_id")
        if not request.form.get("personnes_amendes_id", "").strip():
            erreurs.append("personnes_amendes_id")
        if not request.form.get("personnes_nom", "").strip():
            erreurs.append("personnes_nom")
        if not request.form.get("personnes_prenom", "").strip():
            erreurs.append("personnes_prenom")

        if not erreurs:
            print("Faire ma modifications")
            ma_personne.personnes_id = request.form["personnes_id"]
            ma_personne.personnes_amendes_id = request.form["personnes_amendes_id"]
            ma_personne.personnes_nom = request.form["personnes_nom"]
            ma_personne.personnes_prenom = request.form["personnes_prenom"]


            db.session.add(ma_personne)
            db.session.add(Authorship(personne=ma_personne, user=current_user))
            db.session.commit()
            updated = True

    return render_template(
        "pages/personne_form_update.html",
        nom="Criminalithé",
        personne=ma_personne,
        erreurs=erreurs,
        updated=updated
    )

@app.route("/amende/<int:amendes_id>/update", methods=["GET", "POST"])
@login_required
def amende_update(amendes_id):

    mon_amende = Amendes.query.get(amendes_id)

    erreurs = []
    updated = False

    if request.method == "POST":
        # J"ai un formulaire
        if not request.form.get("amendes_id", "").strip():
            erreurs.append("amendes_id")
        if not request.form.get("amendes_source_id", "").strip():
            erreurs.append("amendes_source_id")
        if not request.form.get("amendes_montant", "").strip():
            erreurs.append("amendes_montant")
        if not request.form.get("amendes_type", "").strip():
            erreurs.append("amendes_type")
        if not request.form.get("amendes_franche_verite", "").strip():
                erreurs.append("amendes_franche_verite")
        if not request.form.get("amendes_transcription", "").strip():
            erreurs.append("amendes_transcription")


        if not erreurs:
            print("Faire ma modifications")
            mon_amende.amendes_id = request.form["amendes_id"]
            mon_amende.amendes_source_id = request.form["amendes_source_id"]
            mon_amende.amendes_montant = request.form["amendes_montant"]
            mon_amende.amendes_type = request.form["amendes_type"]
            mon_amende.amendes_franche_verite = request.form["amendes_franche_verite"]
            mon_amende.amendes_transcription = request.form["amendes_transcription"]


            db.session.add(mon_amende)
            db.session.add(Authorship(amende=mon_amende, user=current_user))
            db.session.commit()
            updated = True

    return render_template(
        "pages/amende_form_update.html",
        nom="Criminalithé",
        amende=mon_amende,
        erreurs=erreurs,
        updated=updated
    )

@app.route("/source/<int:source_id>/update", methods=["GET", "POST"])
@login_required
def source_update(source_id):

    ma_source = Source.query.get(source_id)

    erreurs = []
    updated = False

    if request.method == "POST":
        # J"ai un formulaire
        if not request.form.get("source_id", "").strip():
            erreurs.append("source_id")
        if not request.form.get("source_date", "").strip():
            erreurs.append("source_date")

        if not erreurs:
            print("Faire ma modifications")
            ma_source.source_id = request.form["source_id"]
            ma_source.source_date = request.form["source_date"]



            db.session.add(ma_source)
            db.session.add(Authorship(source=ma_source, user=current_user))
            db.session.commit()
            updated = True

    return render_template(
        "pages/source_form_update.html",
        nom="Criminalithé",
        source=ma_source,
        erreurs=erreurs,
        updated=updated
    )




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
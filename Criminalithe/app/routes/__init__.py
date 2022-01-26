from flask import Flask, render_template, request, flash, redirect

from ..app import app, login, db
from ..modeles.donnees import Source, Amendes, Personnes, Authorship
from ..modeles.utilisateurs import User
from sqlalchemy import and_, or_
from ..constantes import RESULTATS_PAR_PAGES
from flask_login import login_user, current_user, logout_user, login_required

#Route menant à la page d'accueil:

@app.route("/")
def accueil():
    return render_template("pages/accueil.html")

#Route menant à l'"index général":

@app.route("/Index/")
def index():
    return render_template("pages/Index.html")

@app.route("/repertoire/")
def repertoire():
    return render_template("pages/repertoire.html")

#Route menant aux différentes pages d'index:

@app.route("/Index/personnes/")
def index_personnes():
    personnes = Personnes.query.all()
    return render_template("pages/Index_personnes.html", personnes=personnes)


@app.route("/Index/sources/")
def index_sources():
    sources = Source.query.all()
    return render_template("pages/Index_sources.html", sources=sources)

@app.route("/Index/amendes/")
def index_amendes():
    amendes = Amendes.query.all()
    return render_template("pages/Index_amendes.html", amendes=amendes)



#Route menant aux différentes pages de contenu:

@app.route("/amende/<int:amendes_id>")
def amende(amendes_id):

    """Création d'une page de contenu pour une amende.
    :param amendes_id: Id de la clé primaire de la table Amendes dans la base de données
    :type: amendes_id: Integer
    :returns: création de la page grâce au render_template
    """
    amende_unique = Amendes.query.filter(Amendes.amendes_id == amendes_id).first()
    return render_template("pages/amende.html", amende=amende_unique)


@app.route("/personne/<int:personnes_id>")
def personne(personnes_id):
    """Création d'une page de contenu pour une personne.
        :param personnes_id: Id de la clé primaire de la table Personnes dans la base de données
        :type personnes_id: Integer
        :returns: création de la page grâce au render_template """

    personne_unique = Personnes.query.filter(Personnes.personnes_id == personnes_id).first()
    return render_template("pages/personne.html", personne=personne_unique)


@app.route("/source/<int:source_id>")
def source(source_id):

    """Création d'une page de contenu pour une source.
        :param source_id: Id de la clé primaire de la table Personnes dans la base de données
        :type source_id: Integer
        :returns: création de la page grâce au render_template """

    source_unique = Source.query.filter(Source.source_id == source_id).first()
    return render_template("pages/source.html", source=source_unique)

#Route pour une page de recherche simple par le biais d'une requête sur la table Amendes.
#Permet d'afficher 5 résultats par page grâce à la méthode .paginate de Flask.

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
        resultats = \
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


#Permet d'afficher une page avec le formulaire d'inscription si l'utilisateur n'est pas encore enregistré dans la base de données.

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

#Permet d'afficher une page de connexion:

@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """
    Route vérifiant si l'utilisateur est déja connecté lorsqu'il s'authentifie
    Si c'est le cas, l'utilisateur est redirigé vers la page d'accueil.
    Sinon, renvoi un formulaire de connexion.
    En cas d'erreurs, affiche un message d'erreurs.
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

#Route permettant la déconnexion de l'utilisateur.

@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e", "info")
    return redirect("/")


#Routes des formulaires de mise à jour des données pour les amendes, personnes et les sources.

@app.route("/personne/<int:personnes_id>/update", methods=["GET", "POST"])
@login_required
def personne_update(personnes_id):

    """
    :param personnes_id: Id de la clé primaire de la table Personnes dans la base de données
    :type personnes_id: Integer
    :return: formulaire de mise à jour des données pour une personne.
    """
    ma_personne = Personnes.query.get(personnes_id)

    erreurs = []
    updated = False

    if request.method == "POST":
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

    """
    :param amendes_id: Id de la clé primaire de la table Amendes dans la base de données
    :type amendes_id: Integer
    :return: formulaire de mise à jour des données pour une amende.
    """

    mon_amende = Amendes.query.get(amendes_id)

    erreurs = []
    updated = False

    if request.method == "POST":
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

    """
    :param source_id: Id de la clé primaire de la table Source dans la base de données
    :type source_id: Integer
    :return: formulaire de mise à jour des données pour une amende.
    """
    ma_source = Source.query.get(source_id)

    erreurs = []
    updated = False

    if request.method == "POST":
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

@app.route("/ajout_amende", methods=["GET", "POST"])
@login_required
def ajout_amende():

    # Ajout d'une amende
    if request.method == "POST":
        statut, informations = Amendes.ajout_amende(
        ajout_amendes_id = request.form.get("ajout_amendes_id", None),
        ajout_amendes_source_id = request.form.get("ajout_amendes_source_id", None),
        ajout_amendes_montant = request.form.get("ajout_amendes_montant", None),
        ajout_amendes_type = request.form.get("ajout_amendes_type", None),
        ajout_amendes_franche_verite = request.form.get("ajout_amendes_franche_verite", None),
        ajout_amendes_transcription= request.form.get("ajout_amendes_transcription", None)
        )

        if statut is True:
            flash("Ajout d'une nouvelle amende", "success")
            return redirect("/")
        else:
            flash("L'ajout a échoué pour les raisons suivantes : " + ", ".join(informations), "danger")
            return render_template("pages/ajout_amende.html")
    else:
        return render_template("pages/ajout_amende.html")

@app.route("/ajout_personne", methods=["GET", "POST"])
@login_required
def ajout_personne():

    # Ajout d'une personne
    if request.method == "POST":
        statut, informations = Personnes.ajout_personne(
        ajout_personnes_id = request.form.get("ajout_personnes_id", None),
        ajout_personnes_amendes_id = request.form.get("ajout_personnes_amendes_id", None),
        ajout_personnes_nom = request.form.get("ajout_personnes_nom", None),
        ajout_personnes_prenom = request.form.get("ajout_personnes_prenom", None)
        )

        if statut is True:
            flash("Ajout d'une nouvelle personne", "success")
            return redirect("/")
        else:
            flash("L'ajout a échoué pour les raisons suivantes : " + ", ".join(informations), "danger")
            return render_template("pages/ajout_personne.html")
    else:
        return render_template("pages/ajout_personne.html")

@app.route("/ajout_source", methods=["GET", "POST"])
@login_required
def ajout_source():

    # Ajout d'une personne
    if request.method == "POST":
        statut, informations = Source.ajout_source(
        ajout_source_id = request.form.get("ajout_source_id", None),
        ajout_source_date = request.form.get("ajout_source_date", None)
        )

        if statut is True:
            flash("Ajout d'une nouvelle source", "success")
            return redirect("/")
        else:
            flash("L'ajout a échoué pour les raisons suivantes : " + ", ".join(informations), "danger")
            return render_template("pages/ajout_source.html")
    else:
        return render_template("pages/ajout_source.html")

@app.route("/supprimer_amende/<int:amendes_id>", methods=["POST", "GET"])
@login_required
def supprimer_amende(amendes_id):

    suppr_amende = Amendes.query.get(amendes_id)

    if request.method == "POST":
        statut = Amendes.supprimer_amende(
            amendes_id=amendes_id
        )

        if statut is True:
            flash("Suppression réussie", "success")
            return redirect("/")
        else:
            flash("La suppression a échoué. Réessayez !", "error")
            return redirect("/")
    else:
        return render_template("pages/supprimer_amende.html", suppr_amende=suppr_amende)

@app.route("/supprimer_personne/<int:personnes_id>", methods=["POST", "GET"])
@login_required
def supprimer_personne(personnes_id):

    suppr_personne = Personnes.query.get(personnes_id)

    if request.method == "POST":
        statut = Personnes.supprimer_personne(
            personnes_id=personnes_id
        )

        if statut is True:
            flash("Suppression réussie", "success")
            return redirect("/")
        else:
            flash("La suppression a échoué. Réessayez !", "error")
            return redirect("/")
    else:
        return render_template("pages/supprimer_personne.html", suppr_personne=suppr_personne)

@app.route("/supprimer_source/<int:source_id>", methods=["POST", "GET"])
@login_required
def supprimer_source(source_id):

    suppr_source = Source.query.get(source_id)

    if request.method == "POST":
        statut = Source.supprimer_source(
            source_id=source_id
        )

        if statut is True:
            flash("Suppression réussie", "success")
            return redirect("/")
        else:
            flash("La suppression a échoué. Réessayez !", "error")
            return redirect("/")
    else:
        return render_template("pages/supprimer_source.html", suppr_source=suppr_source)
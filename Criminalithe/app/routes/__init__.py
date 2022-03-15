from flask import Flask, render_template, request, flash, redirect, send_file, url_for
# L'import de flash permet d'afficher des messages d'alertes en "pop-up".
# L'import de redirect permet de rediriger vers une page spécifique dans le return-template.
# L'import de send_file permet des fichiers au client; nous l'utilisons pour permettre de télécharger la BDD sous divers formats.

from ..app import app, login, db
# Importe les variables app, login et db qui instancient notre application.
from ..modeles.donnees import Source, Amendes, Personnes, Authorship
# Importe les modèles de données de notre BDD
from ..modeles.utilisateurs import User
# Importe les modèles de données de notre BDD consacrée aux utilisateurs

from sqlalchemy import and_, or_
# L'import de _and et _or permet d'utiliser les opérateurs booléens and et or dans les fonctions de requêtes sur la BDD.

from ..constantes import RESULTATS_PAR_PAGES, RESULTATS_PAR_PAGES_INDEX, RESULTATS_PAR_PAGES_RECHERCHE_AVANCEE
# Importe le nombre de résultats par pages de manière différenciée.
from flask_login import login_user, current_user, logout_user, login_required
# Import permettant de gérer les connexions et déconnexion des utilisateurs de l'application.
from warnings import warn
# Import permettant d'afficher des messages d'erreurs.
import random
# Import qui permet de générer des entiers aléatoires; nous l'utilisons pour la fonction de navigation aléatoire dans la BDD.


#Route menant à la page d'accueil.

@app.route("/")
def accueil():
    return render_template("pages/accueil.html")

#Route menant à l'index général, comprenant des urls redirigeant vers les index spécifiques.

@app.route("/Index/")
def index():
    return render_template("pages/Index.html")

#Route menant au répertoire des formulaires d'ajout des données.

@app.route("/repertoire/")
def repertoire():
    return render_template("pages/repertoire.html")

#Route menant au répertoire des formulaires de recherce.

@app.route("/repertoire_recherche_avancee/")
def repertoire_recherche_avancee():
    return render_template("pages/repertoire_recherche_avancee.html")

#Route menant aux différentes pages d'index (personnes, sources et amendes):

@app.route("/Index/personnes/")
def index_personnes():
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    personnes = Personnes.query.order_by(Personnes.personnes_nom).paginate(page=page, per_page=RESULTATS_PAR_PAGES_INDEX)
    return render_template("pages/Index_personnes.html", personnes=personnes)


@app.route("/Index/sources/")
def index_sources():
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    sources = Source.query.paginate(page=page, per_page=RESULTATS_PAR_PAGES_INDEX)
    return render_template("pages/Index_sources.html", sources=sources)

@app.route("/Index/amendes/")
def index_amendes():

    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1


    amendes = Amendes.query.paginate(page=page, per_page=RESULTATS_PAR_PAGES_INDEX)

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
#La méthode .like() permet d'élargir le champs de recherche.
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
#Nous utilisons flahs pour indiquer le succès ou les erreurs liées à l'inscription et redirect pour renvoyer l'utilisateur soit sur la page
#d'accueil une fois l'inscription réussie, soit vers cette même page en cas d'erreurs.
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

#Permet d'afficher une page de connexion :
# - Route vérifiant si l'utilisateur est déja connecté lorsqu'il s'authentifie
# - Si c'est le cas, l'utilisateur est redirigé vers la page d'accueil (avec redirect)
# - Sinon, renvoi un formulaire de connexion (avec redirect)
# - En cas d'erreurs, affiche un message d'erreurs (avec flash)

@app.route("/connexion", methods=["POST", "GET"])
def connexion():



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

#Route permettant la déconnexion de l'utilisateur; utilisation de la fonction importée logout_user() pour gérer la déconnexion.

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


#Route permettant l'ajout d'une amende dans la BDD.
#Nous utilisons la méthode statique @login_required pour en limiter l'accès aux utilisateurs inscrits et connectés.
#Nous appelons la méthode statique .ajout_amende issue de notre modéle de données.

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
        return render_template("pages/ajout_amende.html", amendes_type=amendes_type)


#Route permettant l'ajout d'une personne dans la BDD.
#Nous utilisons la méthode statique @login_required pour en limiter l'accès aux utilisateurs inscrits et connectés.
#Nous appelons la méthode statique .ajout_personne issue de notre modéle de données.

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


#Route permettant l'ajout d'une source dans la BDD.
#Nous utilisons la méthode statique @login_required pour en limiter l'accès aux utilisateurs inscrits et connectés.
#Nous appelons la méthode statique .ajout_source issue de notre modéle de données.

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


#Route permettant la suppresion d'une amende dans la BDD.
#Nous utilisons la méthode statique @login_required pour en limiter l'accès aux utilisateurs inscrits et connectés.
#Nous appelons la méthode statique .supprimer_amende issue de notre modéle de données.

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


#Route permettant la suppression d'une personne dans la BDD.
#Nous utilisons la méthode statique @login_required pour en limiter l'accès aux utilisateurs inscrits et connectés.
#Nous appelons la méthode statique .supprimer_personne issue de notre modéle de données.

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

#Route permettant la suppression d'une source dans la BDD.
#Nous utilisons la méthode statique @login_required pour en limiter l'accès aux utilisateurs inscrits et connectés.
#Nous appelons la méthode statique .supprimer_source issue de notre modéle de données.


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

#Route permettant une recherche 'semi-avancée' par le biais de formulaires requêtant en .like() les attributs de la table concernée.

@app.route('/rechercheavancee', methods=["POST", "GET"])
def rechercheavancee():
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    if request.method == "POST":

        keyword = "test"
        resultats_amendes = []

        questionAmendes = Amendes.query

        idAmende = request.form.get("idAmende", None)
        idSourceAmende = request.form.get("idSourceAmende", None)
        montantAmende = request.form.get("montantAmende", None)
        typeAmende = request.form.get("typeAmende", None)
        francheVeriteAmende = request.form.get("francheVeriteAmende", None)
        transcriptionAmende = request.form.get("transcriptionAmende", None)
        idPersonneAmende = request.form.get("idPersonneAmende", None)
        #nomPersonne = request.form.get("nomPersonne", None)


        if idAmende:
            questionAmendes = questionAmendes.filter(Amendes.amendes_id.like("%{}%".format(idAmende)))

        if idSourceAmende:
            questionAmendes = questionAmendes.filter(Amendes.amendes_source_id.like("%{}%".format(idSourceAmende)))

        if montantAmende:
            questionAmendes = questionAmendes.filter(Amendes.amendes_montant.like("%{}%".format(montantAmende)))

        if typeAmende:
            questionAmendes = questionAmendes.filter(Amendes.amendes_type.like("%{}%".format(typeAmende)))

        if francheVeriteAmende:
            questionAmendes = questionAmendes.filter(
                Amendes.amendes_franche_verite.like("%{}%".format(francheVeriteAmende)))

        if transcriptionAmende:
            questionAmendes = questionAmendes.filter(
                Amendes.amendes_transcription.like("%{}%".format(transcriptionAmende)))

        if idPersonneAmende:
            questionAmendes = questionAmendes.filter(Amendes.amendes_personnes_id.like("%{}%".format(idPersonneAmende)))

        #Tentative de requêter également sur les données des jointures, en l'occurence les personnes mentionnées dans les amendes.
        #Cependant, cette technique ne fonctionne pas. Nous en déduisons que les données issues des jointures
        #ne sont pas requêtable directement par le biais de SQLAlchemy :

        # if nomPersonne:
        #     questionAmendes = questionAmendes.filter(Amendes.justiciable.like("%{}%".format(nomPersonne)))

        #Pour une question de lisibilité des résultats, tout les résultats doivent apparaitrent sur une seule page, d'où le recours à cette constante.
        resultats_amendes = questionAmendes.paginate(page=page, per_page=RESULTATS_PAR_PAGES_RECHERCHE_AVANCEE)


        if resultats_amendes is None:
            warn("Vous devez renseigner au moins un élément dans cette catéorie")


        return render_template(
            "pages/resultats_recherche_avancee.html",
            resultats_amendes=resultats_amendes,
        )

    return render_template("pages/rechercheavancee.html", page=page)


#Route permettant une recherche 'semi-avancée' par le biais de formulaires requêtant en .like() les attributs de la table concernée.

@app.route('/rechercheavancee_personnes', methods=["POST", "GET"])
def rechercheavancee_personnes():
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    if request.method == "POST":

        keyword = "test"
        resultats_amendes = []

        questionPersonnes = Personnes.query

        # Amende
        idPersonne = request.form.get("idPersonne", None)
        idPersonneAmende = request.form.get("idPersonneAmende", None)
        nomPersonne = request.form.get("nomPersonne", None)
        prenomPersonne = request.form.get("prenomPersonne", None)



        if idPersonne:
            questionPersonnes = questionPersonnes.filter(Personnes.personnes_id.like("%{}%".format(idPersonne)))

        if idPersonneAmende:
            questionPersonnes = questionPersonnes.filter(Personnes.personnes_amendes_id.like("%{}%".format(idPersonneAmende)))

        if nomPersonne:
            questionPersonnes = questionPersonnes.filter(Personnes.personnes_nom.like("%{}%".format(nomPersonne)))

        if prenomPersonne:
            questionPersonnes = questionPersonnes.filter(Personnes.personnes_prenom.like("%{}%".format(prenomPersonne)))


        #Pour une question de lisibilité des résultats, tout les résultats doivent apparaitrent sur une seule page, d'où le recours à cette constante.
        resultats_personnes = questionPersonnes.paginate(page=page, per_page=RESULTATS_PAR_PAGES_RECHERCHE_AVANCEE)


        if resultats_personnes is None:
            warn("Vous devez renseigner au moins un élément dans cette catéorie")


        return render_template(
            "pages/resultats_recherche_avancee_personnes.html",
            resultats_personnes=resultats_personnes,
        )

    return render_template("pages/rechercheavancee_personnes.html", page=page)


#Route permettant une recherche 'semi-avancée' par le biais de formulaires requêtant en .like() les attributs de la table concernée.

@app.route('/rechercheavancee_source', methods=["POST", "GET"])
def rechercheavancee_source():
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    if request.method == "POST":

        keyword = "test"
        resultats_source = []

        questionSource = Source.query

        # Amende
        idSource = request.form.get("idSource", None)
        dateSource = request.form.get("dateSource", None)




        if idSource:
            questionSource = questionSource.filter(Source.source_id.like("%{}%".format(idSource)))

        if dateSource:
            questionSource = questionSource.filter(Source.source_date.like("%{}%".format(dateSource)))

        #Pour une question de lisibilité des résultats, tout les résultats doivent apparaitrent sur une seule page, d'où le recours à cette constante.
        resultats_source = questionSource.paginate(page=page, per_page=RESULTATS_PAR_PAGES_RECHERCHE_AVANCEE)


        if resultats_source is None:
            warn("Vous devez renseigner au moins un élément dans cette catéorie")


        return render_template(
            "pages/resultats_recherche_avancee_source.html",
            resultats_source=resultats_source,
        )

    return render_template("pages/rechercheavancee_source.html", page=page)

#Route menant à la page de téléchargement de la BDD.

@app.route('/telechargement')
def telechargement():
    return render_template("pages/telechargement.html")

#Route envoyant avec return send_file la BDD à l'utilisateur au format SQLite.

@app.route('/download')
def download():
    f = './bdd2.db'
    return send_file(f, attachment_filename='bdd2.db', as_attachment=True)

#Route envoyant avec return send_file la BDD à l'utilisateur au format SQL.


@app.route('/download_sql')
def download_sql():
    f = './bdd2.sql'
    return send_file(f, attachment_filename='bdd2.sql', as_attachment=True)

#Route donnant accès à la page de navigation dans l'API.
#Sur celle-ci, trois formulaires permettent de requêter l'API pour la table amendes, personnes et sources.

@app.route("/navigation_api")
def navigation_api():

    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    resultats_amendes = Amendes.query.paginate(page=page, per_page=RESULTATS_PAR_PAGES)
    resultats_personnes = Personnes.query.paginate(page=page, per_page=RESULTATS_PAR_PAGES)
    resultats_source = Source.query.paginate(page=page, per_page=RESULTATS_PAR_PAGES)

    return render_template(
        "pages/navigation_api.html",
        resultats_amendes=resultats_amendes,
        resultats_personnes=resultats_personnes,
        resultats_source=resultats_source
    )

#Permet avec errorhandler d'afficher le code status HTTP approprié en cas d'erreur et de renvoyer vers
#la page erreur 404.

@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html', nom="404 - Page non trouvée"), 404


#Permet avec errorhandler d'afficher le code status HTTP approprié en cas d'erreur et de renvoyer vers
#la page erreur 404.

@app.errorhandler(418)
def page_not_found(e):
    return render_template('pages/404.html', nom="418 - I am a teapot"), 418


# Route génère un nombre aléatoire, et retourne une redirection vers l'url composée de noticechercheur et de ce nombre aléatoire,
# ce qui déclenche de là la fonction noticechercheur prenant ce nombre aléatoire en paramètre : cela affiche donc une notice aléatoirement
#

@app.route('/aleatoire')
def aleatoire():

    nbMax = Amendes.query.count()

    nb = random.randint(1, nbMax)

    return redirect(url_for('amende', amendes_id=nb))


#Route cachée quelque part dans l'application qui permet d'afficher la fameuse erreur 418 "I am a teapot".

@app.route("/418")
def teapot():
    return render_template("pages/418.html")
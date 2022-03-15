from flask import render_template, request, url_for, jsonify
#Import de jsonify permet de renvoyer les données au format JSON.
from urllib.parse import urlencode
#Import d'urlencode utilisé pour encoder les paramètres GET des url via un dictionnaire.

from ..app import app
# Importe les variables app instancie notre application.

from ..modeles.donnees import Source, Amendes, Personnes, Authorship
# Importe les modèles de données de notre BDD

from ..modeles.utilisateurs import User
# Importe les modèles de données de notre BDD utilisateurs

from ..constantes import RESULTATS_PAR_PAGES, API_ROUTE
#Import des constantes du nombres de résultats par page et de la constante
#de la route de l'API


#Route renvoyant une erreur 404 lorsque la requête est erronée ou ne pas renvoyer
#de données en JSON

def Json_404():
    response = jsonify({"erreur": "Unable to perform the query"})
    response.status_code = 404
    return response

#Route permettant de renvoyer les données issue des amendes au format JSON.

@app.route(API_ROUTE+"/amende/<amendes_id>")
def api_amendes(amendes_id):
    try:
        query = Amendes.query.get(amendes_id)
        return jsonify(query.amendes_to_jsonapi_dict())
    except:
        return Json_404()

#Route permettant de renvoyer les données issue des amendes au format JSON.

@app.route(API_ROUTE+"/source/<source_id>")
def api_source(source_id):
    try:
        query = Source.query.get(source_id)
        return jsonify(query.source_to_jsonapi_dict())
    except:
        return Json_404()

#Route permettant de renvoyer les données issue des amendes au format JSON.

@app.route(API_ROUTE+"/personne/<personnes_id>")
def api_personnes(personnes_id):
    try:
        query = Personnes.query.get(personnes_id)
        return jsonify(query.personnes_to_jsonapi_dict())
    except:
        return Json_404()


#Route permettant de naviguer directement dans la BDD des amendes
# au format JSon ainsi que d'effectuer une recherche plein-texte

@app.route(API_ROUTE+"/amendes")
def api_amendes_navigation():


    # q est très souvent utilisé pour indiquer une capacité de recherche
    motclef = request.args.get("q", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    if motclef:
        query = Amendes.query.filter(
            Amendes.amendes_id.like("%{}%".format(motclef))
        )
    else:
        query = Amendes.query

    try:
        resultats = query.paginate(page=page, per_page=RESULTATS_PAR_PAGES)
    except Exception:
        return Json_404()

    dict_resultats = {
        "links": {
            "self": request.url
        },
        "data": [
            amende.amendes_to_jsonapi_dict()
            for amende in resultats.items
        ]
    }

    if resultats.has_next:
        arguments = {
            "page": resultats.next_num
        }
        if motclef:
            arguments["q"] = motclef
        dict_resultats["links"]["next"] = url_for("api_amendes_navigation", _external=True)+"?"+urlencode(arguments)

    if resultats.has_prev:
        arguments = {
            "page": resultats.prev_num
        }
        if motclef:
            arguments["q"] = motclef
        dict_resultats["links"]["prev"] = url_for("api_amendes_navigation", _external=True)+"?"+urlencode(arguments)

    response = jsonify(dict_resultats)
    return response

#Route permettant de naviguer directement dans la BDD des personnes
# au format JSon ainsi que d'effectuer une recherche plein-texte

@app.route(API_ROUTE+"/personnes")
def api_personnes_navigation():

    motclef = request.args.get("q", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    if motclef:
        query = Personnes.query.filter(
            Personnes.personnes_id.like("%{}%".format(motclef))
        )
    else:
        query = Personnes.query

    try:
        query = query.paginate(page=page, per_page=RESULTATS_PAR_PAGES)
    except Exception:
        return Json_404()

    dict_resultats = {
        "links": {
            "self": request.url
        },
        "data": [
            personne.personnes_to_jsonapi_dict()
            for personne in query.items
        ]
    }

    if query.has_next:
        arguments = {
            "page": query.next_num
        }
        if motclef:
            arguments["q"] = motclef
        dict_resultats["links"]["next"] = url_for("api_personnes_navigation", _external=True)+"?"+urlencode(arguments)

    if query.has_prev:
        arguments = {
            "page": query.prev_num
        }
        if motclef:
            arguments["q"] = motclef
        dict_resultats["links"]["prev"] = url_for("api_personnes_navigation", _external=True)+"?"+urlencode(arguments)

    response = jsonify(dict_resultats)
    return response

#Route permettant de naviguer directement dans la BDD des sources
# au format JSon ainsi que d'effectuer une recherche plein-texte

@app.route(API_ROUTE+"/source")
def api_source_navigation():

    query = request.args.get("q", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    if query:
        query = Source.query.filter(
            Source.source_id.like("%{}%".format(query))
        )
    else:
        query = Source.query

    try:
        query = query.paginate(page=page, per_page=RESULTATS_PAR_PAGES)
    except Exception:
        return Json_404()

    dict_resultats = {
        "links": {
            "self": request.url
        },
        "data": [
            source.source_to_jsonapi_dict()
            for source in query.items
        ]
    }

    if query.has_next:
        arguments = {
            "page": query.next_num
        }
        if motclef:
            arguments["q"] = query
        dict_resultats["links"]["next"] = url_for("api_source_navigation", _external=True)+"?"+urlencode(arguments)

    if query.has_prev:
        arguments = {
            "page": query.prev_num
        }
        if motclef:
            arguments["q"] = query
        dict_resultats["links"]["prev"] = url_for("api_source_navigation", _external=True)+"?"+urlencode(arguments)

    response = jsonify(dict_resultats)
    return response
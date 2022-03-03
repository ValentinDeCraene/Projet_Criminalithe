from flask import render_template, request, url_for, jsonify
from urllib.parse import urlencode

from ..app import app
from ..modeles.donnees import Source, Amendes, Personnes, Authorship
from ..modeles.utilisateurs import User
from ..constantes import RESULTATS_PAR_PAGES, API_ROUTE


def Json_404():
    response = jsonify({"erreur": "Unable to perform the query"})
    response.status_code = 404
    return response

@app.route(API_ROUTE+"/amende/<amendes_id>")
def api_amendes(amendes_id):
    try:
        query = Amendes.query.get(amendes_id)
        return jsonify(query.amendes_to_jsonapi_dict())
    except:
        return Json_404()

@app.route(API_ROUTE+"/source/<source_id>")
def api_source(source_id):
    try:
        query = Source.query.get(source_id)
        return jsonify(query.source_to_jsonapi_dict())
    except:
        return Json_404()

@app.route(API_ROUTE+"/personne/<personnes_id>")
def api_personnes(personnes_id):
    try:
        query = Personnes.query.get(personnes_id)
        return jsonify(query.personnes_to_jsonapi_dict())
    except:
        return Json_404()

@app.route(API_ROUTE+"/amendes")
def api_amendes_navigation():
    """ Route permettant la recherche plein-texte et la navigation classique

    On s'inspirera de http://jsonapi.org/ faute de pouvoir trouver temps d'y coller à 100%
    """
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
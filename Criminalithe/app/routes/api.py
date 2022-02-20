from flask import render_template, request, url_for, jsonify
from urllib.parse import urlencode

from ..app import app
from ..constantes import RESULTATS_PAR_PAGES, API_ROUTE
from ..modeles.donnees import Source, Amendes, Personnes

def Json_404():
    response = jsonify({"erreur": "Unable to perform the query"})
    response.status_code = 404
    return response

@app.route(API_ROUTE+"/amendes/<amendes_id>")
def api_amendes(amendes_id):
    try:
        query = Amendes.query.get(amendes_id)
        return jsonify(query.to_jsonapi_dict())
    except:
        return Json_404()

@app.route(API_ROUTE+"/source/<source_id>")
def api_source(amendes_id):
    try:
        query = Source.query.get(source_id)
        return jsonify(query.to_jsonapi_dict())
    except:
        return Json_404()

@app.route(API_ROUTE+"/personnes/<personnes_id>")
def api_personnes(personnes_id):
    try:
        query = Personnes.query.get(personnes_id_id)
        return jsonify(query.to_jsonapi_dict())
    except:
        return Json_404()
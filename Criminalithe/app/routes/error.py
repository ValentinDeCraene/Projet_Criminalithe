from flask import render_template
from ..app import app

# Routes erreurs courantes

@app.errorhandler(401)
def unauthorized_error(error):
    """
    Route qui permet d'afficher la page 401.html en cas d'erreur 401 (accès non autorisé)
    :return: template 401.html
    """
    return render_template('errors/401.html'), 401


@app.errorhandler(404)
def not_found_error(error):
    """
    Route qui permet d'afficher la page 404.html en cas d'erreur 404 (page introuvable)
    :return: template 404.html
    """
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Route qui permet d'afficher la page 500.html en cas d'erreur 500 (erreur de serveur interne)
    :return: template 500.html
    """
    return render_template('errors/500.html'), 500
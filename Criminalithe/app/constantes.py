from warnings import warn

API_ROUTE = "/api"

#La variable résultats par page est déclarée ici pour afficher 5 résultats par page lors de l'utilisation de la méthode .paginate
RESULTATS_PAR_PAGES = 10

RESULTATS_PAR_PAGES_INDEX= 10

RESULTATS_PAR_PAGES_RECHERCHE_AVANCEE = 130
#Jacques Le Goff l'a démontré :
SECRET_KEY = "L'EPOQUE MODERNE N'EST QU'UN LONG MOYEN AGE"

if SECRET_KEY == "L'EPOQUE MODERNE N'EST QU'UN LONG MOYEN AGE":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)
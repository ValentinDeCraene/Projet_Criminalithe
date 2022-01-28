from warnings import warn


#La variable résultats par page est déclarée ici pour afficher 5 résultats par page lors de l'utilisation de la méthode .paginate
RESULTATS_PAR_PAGES = 5

RESULTATS_PAR_PAGES_INDEX= 10

#Jacques Le Goff l'a démontré :
SECRET_KEY = "L'EPOQUE MODERNE N'EST QU'UN LONG MOYEN AGE"

if SECRET_KEY == "L'EPOQUE MODERNE N'EST QU'UN LONG MOYEN AGE":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)
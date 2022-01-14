from warnings import warn

RESULTATS_PAR_PAGES = 5
SECRET_KEY = "SECRET KEY"

if SECRET_KEY == "SECRET KEY":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)
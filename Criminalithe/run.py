from app.app import app, config_app

# Lance l'application
# Le mode debug permet de lancer un débogueur pendant le développement de l'application

if __name__ == "__main__":
    app = config_app("production")
    app.run(debug=True)


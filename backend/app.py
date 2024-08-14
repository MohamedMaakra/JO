from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from routes.offers import bp as offers_bp  # Assurez-vous que le fichier offers.py est dans le même répertoire que app.py

# Créer une instance de SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuration de la base de données
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/jo'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CORS_HEADERS'] = 'Content-Type'

    # Initialiser SQLAlchemy avec l'application
    db.init_app(app)

    # Configurer les CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Enregistrer les blueprints
    app.register_blueprint(offers_bp)

    # Autres configurations ou blueprints peuvent être ajoutés ici

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

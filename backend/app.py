from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from routes.auth import auth_bp
from routes.offers import offers_bp
import os
from dotenv import load_dotenv

def create_app():
    load_dotenv()  # Charger les variables d'environnement depuis .env
    
    app = Flask(__name__)

    # Configuration de la base de données
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///local.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key_here')  # Clé secrète pour JWT

    # Initialiser SQLAlchemy avec l'application
    db.init_app(app)

    # Configurer les CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Enregistrer les blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(offers_bp, url_prefix='/api/offers')

    # Ajouter une route Hello World
    @app.route('/hello', methods=['GET'])
    def hello_world():
        return jsonify(message="Hello World")

    # Ajouter la route de test
    @app.route('/test', methods=['GET'])
    def test_route():
        return jsonify(message="Test route is working")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Port par défaut 5000

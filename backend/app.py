from flask import Flask
from flask_cors import CORS
from models import db
from routes.offers import offers_bp  # Importer le blueprint des offres
from routes.cart import cart_bp  # Importer le blueprint du panier
from routes.auth import auth_bp  # Importer le blueprint d'authentification

def create_app():
    app = Flask(__name__)

    # Configuration de la base de données
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/jo'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Clé secrète pour JWT

    # Initialiser SQLAlchemy avec l'application
    db.init_app(app)

    # Configurer les CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Enregistrer les blueprints
    app.register_blueprint(offers_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(auth_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
from datetime import timedelta, datetime as dt

# Initialiser l'instance SQLAlchemy
db = SQLAlchemy()

# Définir le modèle User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    key = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    failed_attempts = db.Column(db.Integer, default=0)
    lockout_time = db.Column(db.DateTime, nullable=True)

# Définir le modèle Offer
class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    prix = db.Column(db.Float, nullable=False)
    details = db.Column(db.Text)
    nombre_personnes = db.Column(db.Integer, default=1)

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

    @app.route('/api/offers', methods=['POST'])
    def create_offer():
        data = request.get_json()
        titre = data.get('titre')
        description = data.get('description')
        prix = data.get('prix')
        details = data.get('details')
        nombre_personnes = data.get('nombre_personnes', 1)  # Nombre de personnes par défaut

        if not titre or not prix:
            return jsonify({"message": "Les champs 'titre' et 'prix' sont requis"}), 400

        try:
            new_offer = Offer(titre=titre, description=description, prix=prix, details=details, nombre_personnes=nombre_personnes)
            db.session.add(new_offer)
            db.session.commit()
            return jsonify({"message": "Nouvelle offre créée avec succès"}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/offers', methods=['GET'])
    def get_offers():
        try:
            offers = Offer.query.all()
            offers_list = [
                {
                    'id': offer.id,
                    'titre': offer.titre,
                    'description': offer.description,
                    'prix': offer.prix,
                    'details': offer.details,
                    'nombre_personnes': offer.nombre_personnes
                }
                for offer in offers
            ]
            return jsonify(offers_list), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/signup', methods=['POST'])
    def signup():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        nom = data.get('nom')
        prenom = data.get('prenom')
        key = data.get('key')  # Assurez-vous de fournir une clé pour l'utilisateur

        if not email or not password or not nom or not prenom or not key:
            return jsonify({"message": "Tous les champs sont requis"}), 400

        hashed_password = generate_password_hash(password, method='sha256')

        try:
            new_user = User(
                email=email,
                password=hashed_password,
                nom=nom,
                prenom=prenom,
                key=key
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "Utilisateur créé avec succès"}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/signin', methods=['POST'])
    def signin():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"message": "Les champs 'email' et 'password' sont requis"}), 400

        user = User.query.filter_by(email=email).first()

        if user and user.lockout_time and user.lockout_time > dt.utcnow():
            return jsonify({"message": "Compte verrouillé. Réessayez plus tard"}), 403

        if user and check_password_hash(user.password, password):
            user.failed_attempts = 0
            user.lockout_time = None
            db.session.commit()

            # Créer le token JWT avec is_admin
            token = jwt.encode({
                'user_id': user.id,
                'is_admin': user.is_admin,  # Inclure is_admin
                'exp': dt.utcnow() + timedelta(hours=1)
            }, app.config['SECRET_KEY'], algorithm='HS256')

            # Ajouter des logs pour le token
            print("Generated Token:", token)
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            print("Decoded Token:", decoded_token)

            return jsonify({
                'message': 'Connexion réussie',
                'token': token,
                'is_admin': user.is_admin
            }), 200
        else:
            if user:
                user.failed_attempts += 1
                if user.failed_attempts >= 5:
                    user.lockout_time = dt.utcnow() + timedelta(minutes=15)
                db.session.commit()
            return jsonify({"message": "Adresse email ou mot de passe incorrect"}), 401


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

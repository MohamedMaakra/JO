from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Offer
import jwt
import datetime

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
            return jsonify({"message": "Email et mot de passe sont requis"}), 400

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            token = jwt.encode(
                {'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )
            return jsonify({"message": "Connexion réussie", "token": token}), 200
        else:
            return jsonify({"message": "Email ou mot de passe incorrect"}), 401

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

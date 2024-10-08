from flask import Blueprint, request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import timedelta, datetime as dt
from functools import wraps
from models import db, User

auth_bp = Blueprint('auth', __name__)

# Décorateur pour vérifier l'authentification
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({"message": "Token manquant"}), 401

        try:
            data = jwt.decode(token, 'your_secret_key_here', algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except Exception as e:
            return jsonify({"message": "Token invalide ou expiré"}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# Route d'inscription
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    nom = data.get('nom')
    prenom = data.get('prenom')
    key = data.get('key')

    if not email or not password or not nom or not prenom or not key:
        return jsonify({"message": "Tous les champs sont requis"}), 400

    hashed_password = generate_password_hash(password, method='sha256')

    try:
        new_user = User(
            email=email,
            password=hashed_password,
            nom=nom,
            prenom=prenom,
            key=key,
            is_admin=False  # Par défaut, l'utilisateur n'est pas un admin
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Utilisateur créé avec succès"}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route de connexion
@auth_bp.route('/signin', methods=['POST'])
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

        token = jwt.encode({
            'user_id': user.id,
            'is_admin': user.is_admin,
            'exp': dt.utcnow() + timedelta(hours=1)
        }, 'your_secret_key_here', algorithm='HS256')

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

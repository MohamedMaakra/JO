from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Offer(db.Model):
    __tablename__ = 'offer'
    __table_args__ = {'schema': 'jo'}
    
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    prix = db.Column(db.Numeric(10, 2), nullable=False)
    details = db.Column(db.Text)
    nombre_personnes = db.Column(db.Integer, nullable=False)

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'jo'}
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    key = db.Column(db.String(36), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    failed_attempts = db.Column(db.Integer, default=0)
    lockout_time = db.Column(db.DateTime)

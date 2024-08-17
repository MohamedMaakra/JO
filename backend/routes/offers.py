from flask import Blueprint, request, jsonify
from models import db, Offer

offers_bp = Blueprint('offers', __name__)

@offers_bp.route('/', methods=['POST'])
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

@offers_bp.route('/', methods=['GET'])
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

@offers_bp.route('/<int:offer_id>', methods=['PUT'])
def update_offer(offer_id):
    data = request.get_json()
    titre = data.get('titre')
    description = data.get('description')
    prix = data.get('prix')
    details = data.get('details')
    nombre_personnes = data.get('nombre_personnes', 1)  # Nombre de personnes par défaut

    offer = Offer.query.get(offer_id)

    if not offer:
        return jsonify({"message": "Offre non trouvée"}), 404

    if titre:
        offer.titre = titre
    if description:
        offer.description = description
    if prix is not None:
        offer.prix = prix
    if details:
        offer.details = details
    if nombre_personnes is not None:
        offer.nombre_personnes = nombre_personnes

    try:
        db.session.commit()
        return jsonify({"message": "Offre mise à jour avec succès"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@offers_bp.route('/<int:offer_id>', methods=['DELETE'])
def delete_offer(offer_id):
    offer = Offer.query.get(offer_id)

    if not offer:
        return jsonify({"message": "Offre non trouvée"}), 404

    try:
        db.session.delete(offer)
        db.session.commit()
        return jsonify({"message": "Offre supprimée avec succès"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

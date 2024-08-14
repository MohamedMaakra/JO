# routes/offers.py

from flask import Blueprint, request, jsonify, current_app

bp = Blueprint('offers', __name__)
    
@bp.route('/api/offers', methods=['POST'])
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
        db = current_app.extensions['sqlalchemy'].db
        cursor = db.session.execute(
            'INSERT INTO offer (titre, description, prix, details, nombre_personnes) VALUES (:titre, :description, :prix, :details, :nombre_personnes)',
            {'titre': titre, 'description': description, 'prix': prix, 'details': details, 'nombre_personnes': nombre_personnes}
        )
        db.session.commit()
        return jsonify({"message": "Nouvelle offre créée avec succès"}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/offers', methods=['GET'])
def get_offers():
    try:
        db = current_app.extensions['sqlalchemy'].db
        offers = db.session.execute('SELECT * FROM offer').fetchall()

        # Formatter les résultats pour une meilleure lisibilité
        offers_list = [
            {
                'id': offer[0],  # Assure-toi que les indices correspondent aux colonnes
                'titre': offer[1],
                'description': offer[2],
                'prix': offer[3],
                'details': offer[4],
                'nombre_personnes': offer[5]
            }
            for offer in offers
        ]

        return jsonify(offers_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

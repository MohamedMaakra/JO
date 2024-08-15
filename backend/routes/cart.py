from flask import Blueprint, request, jsonify
from models import db, Offer, Cart

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    offer_id = data.get('offer_id')
    
    if not offer_id:
        return jsonify({"message": "L'ID de l'offre est requis"}), 400
    
    try:
        offer = Offer.query.get(offer_id)
        if not offer:
            return jsonify({"message": "Offre non trouvée"}), 404
        
        cart_item = Cart(offer_id=offer.id, user_id=1)  # Remplacez user_id=1 par l'ID de l'utilisateur authentifié
        db.session.add(cart_item)
        db.session.commit()
        
        return jsonify({"message": "Offre ajoutée au panier"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

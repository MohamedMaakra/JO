import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/OfferPages.css';
import { CartContext } from '../contexts/CartContext';

const OfferPage = () => {
  const { addToCart } = useContext(CartContext);
  const [offers, setOffers] = useState([]);
  const apiUrl = process.env.REACT_APP_API_URL;

  useEffect(() => {
    const fetchOffers = async () => {
      try {
        if (!apiUrl) {
          throw new Error('API_URL is not defined');
        }
        console.log(`API URL: ${apiUrl}`);
        console.log(`Fetching offers from ${apiUrl}/api/offers`);

        const response = await axios.get(`${apiUrl}/api/offers`);
        console.log("Données reçues : ", response.data);
        setOffers(response.data);
      } catch (error) {
        console.error('Erreur lors de la récupération des offres :', error);
      }
    };

    fetchOffers(); 
  }, [apiUrl]);

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">Nos Offres</h2>
      <div className="row">
        {offers.length > 0 ? (
          offers.map((offer, index) => (
            <div key={offer.id || index} className="col-md-4">
              <div className="card mb-4">
                <div className="card-body">
                  <h5 className="card-title">{offer.titre}</h5>
                  <p className="card-text">{offer.description}</p>
                  <p className="card-text"><strong>{offer.prix} €</strong></p>
                  <p className="card-text">{offer.details}</p>
                  <button
                    className="btn btn-primary w-100"
                    onClick={() => addToCart(offer)}
                  >
                    Choisir cette offre
                  </button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <p className="col">Aucune offre disponible.</p>
        )}
      </div>
    </div>
  );
};

export default OfferPage;

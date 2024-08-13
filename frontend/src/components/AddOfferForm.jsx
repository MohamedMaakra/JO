import React, { useState } from 'react';
import axios from 'axios';

const AddOfferForm = ({ fetchOffers }) => {
  const [formData, setFormData] = useState({
    titre: '',
    description: '',
    prix: '',
    details: '',
    nombre_personnes: 1,
  });
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/offers', formData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      setMessage('Offre ajoutée avec succès');
      setFormData({
        titre: '',
        description: '',
        prix: '',
        details: '',
        nombre_personnes: 1,
      });
      fetchOffers(); // Mettre à jour la liste des offres en appelant fetchOffers
    } catch (error) {
      console.error('Erreur lors de l\'envoi du formulaire:', error);
      setMessage('Erreur lors de l\'envoi du formulaire. Veuillez réessayer.');
    }
  };

  return (
    <div className="card mt-5">
      <div className="card-body">
        <h2 className="card-title text-center">Ajouter une nouvelle offre</h2>
        {message && <div className="alert alert-info">{message}</div>}
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="titre" className="form-label">Titre</label>
            <input
              type="text"
              className="form-control"
              id="titre"
              name="titre"
              value={formData.titre}
              onChange={handleChange}
              placeholder="Entrez le titre de l'offre"
              required
            />
          </div>
          <div className="mb-3">
            <label htmlFor="description" className="form-label">Description</label>
            <textarea
              className="form-control"
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Entrez la description de l'offre"
              required
            />
          </div>
          <div className="mb-3">
            <label htmlFor="prix" className="form-label">Prix</label>
            <input
              type="number"
              className="form-control"
              id="prix"
              name="prix"
              value={formData.prix}
              onChange={handleChange}
              placeholder="Entrez le prix de l'offre"
              required
            />
          </div>
          <div className="mb-3">
            <label htmlFor="details" className="form-label">Détails</label>
            <textarea
              className="form-control"
              id="details"
              name="details"
              value={formData.details}
              onChange={handleChange}
              placeholder="Entrez les détails de l'offre"
              required
            />
          </div>
          <div className="mb-3">
            <label htmlFor="nombre_personnes" className="form-label">Nombre de personnes</label>
            <input
              type="number"
              className="form-control"
              id="nombre_personnes"
              name="nombre_personnes"
              value={formData.nombre_personnes}
              onChange={handleChange}
              placeholder="Entrez le nombre de personnes pour l'offre"
              required
            />
          </div>
          <button type="submit" className="btn btn-primary w-100">
            Ajouter l'offre
          </button>
        </form>
      </div>
    </div>
  );
};

export default AddOfferForm;

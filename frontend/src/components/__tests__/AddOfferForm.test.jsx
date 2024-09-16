import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import axios from 'axios';
import AddOfferForm from '../AddOfferForm';

// Mock axios
jest.mock('axios');

describe('AddOfferForm', () => {
  beforeEach(() => {
    jest.resetAllMocks(); // Réinitialiser les mocks avant chaque test
  });

  test('renders the form with initial empty values', () => {
    render(<AddOfferForm fetchOffers={() => {}} />);

    expect(screen.getByLabelText(/Titre/i)).toHaveValue('');
    expect(screen.getByLabelText(/Description/i)).toHaveValue('');
    expect(screen.getByLabelText(/Prix/i)).toHaveValue('');
    expect(screen.getByLabelText(/Détails/i)).toHaveValue('');
    expect(screen.getByLabelText(/Nombre de personnes/i)).toHaveValue(1);
  });

  test('allows user to fill in the form and submit', async () => {
    axios.post.mockResolvedValue({ data: {} }); // Mock de la réponse de l'API

    render(<AddOfferForm fetchOffers={() => {}} />);

    fireEvent.change(screen.getByLabelText(/Titre/i), { target: { value: 'Nouvelle offre' } });
    fireEvent.change(screen.getByLabelText(/Description/i), { target: { value: 'Description de l\'offre' } });
    fireEvent.change(screen.getByLabelText(/Prix/i), { target: { value: '100' } });
    fireEvent.change(screen.getByLabelText(/Détails/i), { target: { value: 'Détails supplémentaires' } });
    fireEvent.change(screen.getByLabelText(/Nombre de personnes/i), { target: { value: '2' } });

    fireEvent.click(screen.getByText(/Ajouter l'offre/i));

    await waitFor(() => {
      expect(axios.post).toHaveBeenCalledWith(
        `${process.env.REACT_APP_API_URL}/api/offers`,
        {
          titre: 'Nouvelle offre',
          description: 'Description de l\'offre',
          prix: '100',
          details: 'Détails supplémentaires',
          nombre_personnes: '2',
        },
        { headers: { 'Content-Type': 'application/json' } }
      );
    });
  });
});
  
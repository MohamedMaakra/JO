import React, { useContext } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from '../contexts/AuthContext'; // Importer `useAuth` au lieu de `AuthContext`
import { CartContext } from '../contexts/CartContext'; 
import 'bootstrap/dist/css/bootstrap.min.css';

const Header = () => {
  const { token, isAdmin, signout } = useAuth(); // Utiliser `useAuth` pour obtenir les valeurs
  const { clearCart } = useContext(CartContext);
  const navigate = useNavigate();

  const handleSignout = () => {
    signout();
    clearCart();
    navigate("/");
  };

  return (
    <header className="bg-dark text-white p-3">
      <nav className="container d-flex justify-content-between align-items-center">
        <h1>Jeux Olympiques 2024</h1>
        <ul className="nav">
          <li className="nav-item">
            <NavLink className="nav-link text-white" exact="true" to="/">Accueil</NavLink>
          </li>
          <li className="nav-item">
            <NavLink className="nav-link text-white" to="/offers">Offres</NavLink>
          </li>

          {isAdmin && (
            <li className="nav-item">
              <NavLink className="nav-link text-white" to="/admin">Admin</NavLink>
            </li>
          )}
          {!token ? (
            <>
              <li className="nav-item">
                <NavLink className="nav-link text-white" to="/signin">Connexion</NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link text-white" to="/signup">Inscription</NavLink>
              </li>
            </>
          ) : (
            <li className="nav-item">
              <button className="nav-link btn btn-link text-white" onClick={handleSignout}>Déconnexion</button>
            </li>
          )}
          <li className="nav-item">
            <NavLink className="nav-link text-white" to="/cart">Panier</NavLink>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;

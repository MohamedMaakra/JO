import React, { createContext, useState, useContext, useEffect } from 'react';
import {jwtDecode }from 'jwt-decode';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [auth, setAuth] = useState({
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token'),
    isAdmin: JSON.parse(localStorage.getItem('isAdmin')) || false,
  });

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const decodedToken = jwtDecode(token);
        console.log('Decoded Token:', decodedToken); // Vérification du contenu du token
        setAuth(prev => ({
          ...prev,
          isAdmin: decodedToken.is_admin || false
        }));
      } catch (error) {
        console.error('Erreur lors de la décodage du token', error);
      }
    }
  }, []);

  const signin = (token, isAdmin) => {
    localStorage.setItem('token', token);
    localStorage.setItem('isAdmin', JSON.stringify(isAdmin));
    console.log('Stored isAdmin in localStorage:', JSON.stringify(isAdmin)); // Log pour vérification
    setAuth({
      token,
      isAuthenticated: true,
      isAdmin
    });
  };

  const signout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('isAdmin');
    setAuth({
      token: null,
      isAuthenticated: false,
      isAdmin: false
    });
  };

  return (
    <AuthContext.Provider value={{ ...auth, signin, signout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
export { AuthContext };

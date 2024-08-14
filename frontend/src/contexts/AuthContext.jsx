import React, { createContext, useState, useContext } from 'react';

const AuthContext = createContext(); 

export const AuthProvider = ({ children }) => {
  const [auth, setAuth] = useState({
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token'),
  });

  const signin = (token) => {
    localStorage.setItem('token', token);
    setAuth({
      token,
      isAuthenticated: true,
    });
  };

  const signout = () => {
    localStorage.removeItem('token');
    setAuth({
      token: null,
      isAuthenticated: false,
    });
  };

  return (
    <AuthContext.Provider value={{ ...auth, signin, signout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook personnalisé pour utiliser le contexte
export const useAuth = () => useContext(AuthContext);

import React, { createContext, useState, useContext } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [auth, setAuth] = useState({ key: null, isAdmin: false, userId: null, token: null });

  const signin = (key, isAdmin, userId, token) => {
    setAuth({ key, isAdmin, userId, token });
  };

  const signout = () => {
    setAuth({ key: null, isAdmin: false, userId: null, token: null });
  };

  return (
    <AuthContext.Provider value={{ auth, signin, signout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
export { AuthContext };

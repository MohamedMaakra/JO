import React, { useContext } from 'react';
import { AuthContext } from '../AuthContext'; 

const AdminComponent = () => {
  const { isAdmin } = useContext(AuthContext);

  return (
    <div>
      {isAdmin() ? (
        <h1>Composant Administrateur</h1>
      ) : (
        <h1>Accès non autorisé</h1>
      )}
    </div>
  );
};

export default AdminComponent; 
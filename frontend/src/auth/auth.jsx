import Cookies from 'js-cookie';

export const signin = (setAuth, key, isAdmin) => {
  setAuth({ key, isAdmin });
  Cookies.set('isAdmin', isAdmin ? 'true' : 'false', {
    expires: 7,
    sameSite: 'None',  // Définir SameSite sur None
    secure: true       // Assurez-vous que secure est à true si vous utilisez HTTPS
  });
};

export const signout = (setAuth) => {
  setAuth({ key: null, isAdmin: false });
  Cookies.remove('isAdmin', {
    sameSite: 'None',  // Définir SameSite sur None
    secure: true       // Assurez-vous que secure est à true si vous utilisez HTTPS
  });
};

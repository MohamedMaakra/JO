import Cookies from 'js-cookie';
import { signin, signout } from './auth';

// Mock des fonctions Cookies
jest.mock('js-cookie');

describe('Auth functions', () => {
  let setAuth;

  beforeEach(() => {
    // Mock de la fonction setAuth
    setAuth = jest.fn();
    Cookies.set.mockClear();
    Cookies.remove.mockClear();
  });

  test('should sign in and set cookies correctly', () => {
    // Appelle la fonction signin
    signin(setAuth, 'userKey123', true);

    // Vérifie que setAuth a été appelé avec les bons arguments
    expect(setAuth).toHaveBeenCalledWith({ key: 'userKey123', isAdmin: true });

    // Vérifie que Cookies.set a été appelé correctement
    expect(Cookies.set).toHaveBeenCalledWith('isAdmin', 'true', {
      expires: 7,
      sameSite: 'None',
      secure: true
    });
  });

  test('should sign out and remove cookies correctly', () => {
    // Appelle la fonction signout
    signout(setAuth);

    // Vérifie que setAuth a été appelé avec les bons arguments
    expect(setAuth).toHaveBeenCalledWith({ key: null, isAdmin: false });

    // Vérifie que Cookies.remove a été appelé correctement
    expect(Cookies.remove).toHaveBeenCalledWith('isAdmin', {
      sameSite: 'None',
      secure: true
    });
  });
});

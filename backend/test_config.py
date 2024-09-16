class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Utilisation de SQLite en mémoire pour les tests
    SQLALCHEMY_TRACK_MODIFICATIONS = False

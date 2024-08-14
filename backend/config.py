class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/jo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'  # Change cette clé pour la sécurité

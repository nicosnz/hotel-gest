import os

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AUTH_DB_URL       = os.getenv('AUTH_DB_URL')
JWT_SECRET_KEY    = os.getenv('JWT_SECRET_KEY', 'change-me')
JWT_ALGORITHM     = 'HS256'
JWT_EXPIRE_MINUTES = int(os.getenv('JWT_EXPIRE_MINUTES', 480))

AUTH_INITIAL_USERNAME = os.getenv('AUTH_INITIAL_USERNAME', 'recepcion')
AUTH_INITIAL_PASSWORD = os.getenv('AUTH_INITIAL_PASSWORD', 'recepcion123')
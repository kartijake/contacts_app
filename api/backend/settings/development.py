from .base import *

print("in development settings")
DEBUG = True
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:5173").split(",")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DATABASE_DIR / os.getenv("DATABASE_NAME", "db.sqlite3"),
    }
}




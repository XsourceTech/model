# gérer la manque de package dans la production
# ce fichier va être lu automatiquement
try:
    from dotenv import load_dotenv

    load_dotenv(verbose=False)
except ImportError:
    pass
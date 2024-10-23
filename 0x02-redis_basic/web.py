import redis
import requests
from functools import wraps
from typing import Callable

# Connexion à Redis
redis_client = redis.Redis()

def cache_page(fn: Callable) -> Callable:
    """Décorateur pour mettre en cache la page et suivre les accès."""
    @wraps(fn)
    def wrapper(url: str) -> str:
        # Créer une clé pour suivre le nombre d'accès à l'URL
        redis_client.incr(f"count:{url}")

        # Vérifier si le contenu est déjà en cache
        cached_page = redis_client.get(f"cached:{url}")
        if cached_page:
            return cached_page.decode('utf-8')

        # Si non, obtenir la page et la mettre en cache avec une expiration de 10 secondes
        result = fn(url)
        redis_client.setex(f"cached:{url}", 10, result)
        return result

    return wrapper

@cache_page
def get_page(url: str) -> str:
    """Récupère le contenu HTML d'une URL."""
    response = requests.get(url)
    return response.text

# Exemple d'utilisation
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    print(get_page(url))
    print(f"Nombre d'accès à l'URL : {redis_client.get(f'count:{url}').decode('utf-8')}")


import requests
import os
from django.core.cache import cache

THE_CAT_API_URL = os.environ.get("CAT_API_URL")

def get_valid_breeds():
    """
    Fetches the list of valid cat breeds from TheCatAPI.
    Caches the result for 24 hours to minimize API calls.
    """
    breeds = cache.get('cat_breeds')
    if not breeds:
        try:
            response = requests.get(THE_CAT_API_URL, timeout=5)
            response.raise_for_status()
            breeds = [breed['name'] for breed in response.json()]
            cache.set('cat_breeds', breeds, 86400)  # 24 hours
        except (requests.RequestException, ValueError, KeyError):
            # If API is down or invalid, return an empty list or handle gracefully
            return []
    return breeds

def validate_breed(breed_name):
    """
    Validates if a breed name exists in the list of breeds from TheCatAPI.
    """
    valid_breeds = get_valid_breeds()
    if not valid_breeds:
        # If we can't fetch breeds, we might want to allow it or fall back
        # For the sake of the test, let's assume it must be validated
        return False
    return breed_name in valid_breeds

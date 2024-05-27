import os
import json
from termcolor import cprint

from utils.constants import CACHE_FILE

response_cache = {}

def check_cache():
    """Check if cache file exists and prompt user for action."""
    if os.path.exists(CACHE_FILE):
        user_input = input("Previous cache detected. Do you want to clear the cache? (y/N): ").strip().lower()
        if user_input == 'y':
            os.remove(CACHE_FILE)
            response_cache.clear()
            cprint("Cache cleared.", 'cyan')
        else:
            with open(CACHE_FILE, 'r') as file:
                response_cache.update(json.load(file))

import redis
import os
import json

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
CACHE_EXPIRATION = int(os.getenv("CACHE_EXPIRATION", "600"))  # Tempo padrão: 10 minutos

cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def set_cache(key: str, value: dict, expiration: int = CACHE_EXPIRATION):
    """Armazena um valor em cache com uma chave específica."""
    cache.setex(key, expiration, json.dumps(value))

def get_cache(key: str):
    """Recupera um valor do cache."""
    value = cache.get(key)
    return json.loads(value) if value else None

def delete_cache(key: str):
    """Remove um item do cache."""
    cache.delete(key)

def flush_cache():
    """Esvazia todo o cache."""
    cache.flushall()

import redis
from .config import redis_port, redis_host

r = redis.Redis(host=redis_host, port=redis_port)

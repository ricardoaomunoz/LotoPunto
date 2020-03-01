import redis
import os

r = redis.Redis(host='localhost', port=6379, db=0)

# """configuration.FLASK_PRINCIPAL_HOST"""
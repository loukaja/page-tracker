import os
from functools import cache

from flask import Flask
from redis import Redis, RedisError

app = Flask(__name__)


@app.get("/")
def index():
    try:
        page_views = redis().incr("page_views")
    except RedisError:
        app.logger.exception("Redis error")
        return "Sorry, something went wrong \N{THINKING FACE}", 500
    else:
        return f"Page views: {page_views}"


@cache
def redis():
    return Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/"))

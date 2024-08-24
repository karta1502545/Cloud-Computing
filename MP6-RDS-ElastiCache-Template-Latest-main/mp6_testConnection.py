import redis
r = redis.Redis(host='mp6-redis.gobtxh.ng.0001.use1.cache.amazonaws.com', port=6379)
r.ping()
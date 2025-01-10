import redis

def get_redis_client():
    return redis.StrictRedis(host="localhost",port=6379, decode_response =True)

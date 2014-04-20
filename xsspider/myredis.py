import redis
import settings

redis = redis.Redis(**settings.REDIS)

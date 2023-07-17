import redis
import json
# import msgpack

class RedisTools:
    redis_url = "redis://redis:6379/0"  # отримуємо URL-адресу Redis з docker-compose.yml

    __redis = redis.from_url(redis_url, decode_responses=True)


    @classmethod
    def set_telegrame(cls, *args, **kwargs):
        id_telegram = kwargs.get('id_telegrame')
        report = dict(
        id_telegram = kwargs.get('id_telegrame'),
        index_station = kwargs.get('index_station'),
        date_telegram = kwargs.get('date_telegram'),
        time_telegram = kwargs.get('time_telegram'),
        gauges_telegrame = kwargs.get('gauges_telegrame'))
        report_serial = json.dumps(kwargs)
        return cls.__redis.hset(str(id_telegram), mapping = report)

    @classmethod
    def get_teleg(cls, id):
        return cls.__redis.hgetall(id)
 
    @classmethod
    def pub(cls,chanel,**kwargs):
        chanel = chanel
        data = json.dumps(kwargs)
        return cls.__redis.publish(channel=chanel, message=data)





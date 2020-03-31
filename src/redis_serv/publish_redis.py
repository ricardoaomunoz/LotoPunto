from . import r as redis
import json

def put_insert_money(cash):
    print("publish money")
    deliver = redis.publish('money-insert', cash)
    if deliver == 0:
        redis.set(name = 'money-insert', value = cash)
    print(f"delivered to {deliver}")
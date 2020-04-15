from . import r as redis
import json

def put_insert_money(cash):
    try:
        print("publish money")
        data = redis.get('money-insert')
        if data:
            data = json.loads(data)
            data["inserted"] = cash
            data["credit"] = data["credit"] + cash
            data["total"] = data["total"] + cash
        else:
            data = {
                "inserted": cash,
                "credit": cash,
                "total": cash
            }
        data = json.dumps(data)
        print(f"data to publish: {data}")
        deliver = redis.publish('money-insert', data)
        redis.set(name = 'money-insert', value = data)
        print(f"delivered to {deliver}")
    except Exception as err:
        print(f"Error:{err}")
        pass

def reset_credit():
    try:
        data = redis.get('money-insert')
        if data:
            data = json.loads(data)
            data["credit"] = 0
        else:
            data = {
                "inserted": 0,
                "credit": 0,
                "total": 0
            }
        data = json.dumps(data)
        print(f"data to publish: {data}")
        deliver = redis.publish('money-insert', data)
        redis.set(name = 'money-insert', value = data)
        print(f"delivered to {deliver}")
    except Exception as err:
        print(f"Error:{err}")
        pass


def put_message(msg, tipo):
    try:
        print("publish msg")
        if tipo == "error":
            redis.publish('message-error', msg)
        elif tipo == "alert":
            redis.publish('message-alert', msg)
        elif tipo == "warning":
            redis.publish('message-warning', msg)
    except Exception as err:
        print(f"Error {err}")
        pass

def put_value_level(ch, route, quantity):
    try:
        print(f"publish value level {ch} {route} {quantity}")
        data = redis.get("value-level")
        print(f"data from value-level: {data}")
        if data:
            data = json.loads(data)
            channel = "channel" + str(ch)
            if channel in data:
                data[channel][0]["route"] = route
                data[channel][0]["quantity"] = quantity
            else:
                data[channel]=[{'route':route, 'quantity':quantity}]
        else:
            channel = "channel" + str(ch)
            data = {
                channel: [
                    {
                        "route":route,
                        "quantity":quantity
                    }
                ]
            }
        data = json.dumps(data)
        print(f"data to publish: {data}")
        redis.publish('value-level', data)
        redis.set(name = 'value-level', value = data)

    except Exception as err:
        print(f"Error:{err}")
        pass



import asyncio
import json
import websockets
from services.udp_write_payout import UDPPORT

USERS = set()
MONEY = {"value": 0}
udpsock = UDPPORT()

def money_insert_event():
    return json.dumps({"type": "money", **MONEY})

def make_payout(amount):
    msg = 'p ' + str(amount)
    udpsock.WriteUDPport(msg)
    # pass
def enable_payput():
    msg = 'e '
    udpsock.WriteUDPport(msg)
def route(channel, amount):
    msg = 'p ' + str(amount)
    udpsock.WriteUDPport(msg)

async def notify_money():
    if USERS:
        message = money_insert_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    USERS.add(websocket)
    # await notify_users()

async def unregister(websocket):
    USERS.remove(websocket)
    # await notify_users()

async def smart_payout(websocket, path):
    await register(websocket)
    try:
        await websocket.send(money_insert_event)
        async for message in websocket:
            data = json.loads(message)
            if data["action"] == "payout":
                amount = data["amount"]
                make_payout(amount)
            elif data["action"] == "enable":
                enable_payput()
            elif data["action"] == "route_channel":
                amount = data["amount"]
                channel = data["channel"]
                route(channel, amount)
            elif data["action"] == "credit":
                MONEY["value"] += int(data["amount"])
                await notify_money()


            

                

    finally:
        await unregister(websocket)


start_server = websockets.serve(smart_payout, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
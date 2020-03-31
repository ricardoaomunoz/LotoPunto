import asyncio
import json
import websockets
import sys
import socket 
import time
# insert at 1, 0 is the script path (or '' in REPL)
# sys.path.insert(1, '/home/ricardo/Loto_Punto/src/service/')
# from udp_write_payout import UDPPORT
# from services.udp_write_payout import UDPPORT

USERS = set()
MONEY = {"value": 0}
readPort = 8080
writePort = 8081
localIP = "127.0.0.1"
bufferSize = 1024




class UDPPORT():
    def __init__(self):
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def WriteUDPport(self, message):
        msg = str.encode(message)
        self.UDPServerSocket.sendto(msg, (localIP, int(writePort)))    

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
        print(money_insert_event())
        print(type(money_insert_event()))
        await websocket.send(money_insert_event())
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
                print("##### Credit action ...")
                MONEY["value"] += int(data["amount"])
                await notify_money()
   
    finally:
        print("Unregiste user....")
        await unregister(websocket)


start_server = websockets.serve(smart_payout, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
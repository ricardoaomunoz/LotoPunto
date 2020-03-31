import socket 
import time
import asyncio
import json
import websockets
import sys
sys.path.append("..")
from redis_serv.publish_redis import put_insert_money

readPort = 8080
writePort = 8081
localIP = "127.0.0.1"
bufferSize = 1024


UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

MONEY = {"amount": 0}

# async def send_money(websocket):
    
#     # async with websockets.connect(uri) as websocket:
#     data = json.dumps({"action": "credit", **MONEY})
#     await websocket.send(data)
#     print(f"> {data}")

#         # greeting = await websocket.recv()
#         # print(f"< {greeting}")



def get_money_value(value):
    value = int(value)
    cash = 0
    if value == 1:
        cash = 1000
    elif value == 2:
        cash = 2000
    elif value == 3:
        cash = 5000
    elif value == 4:
        cash = 10000
    elif value == 5:
        cash = 20000
    elif value == 6:
        cash = 50000
    return cash

async def ReadUDPport():
    # uri = "ws://localhost:6789"
    # websocket = websockets.connect(uri)
    # Bind to address and ip
    UDPServerSocket.bind((localIP, readPort))
    print("UDP server up and listening")
    # async with websockets.connect(uri) as websocket:
    # data = json.dumps({"action": "credit", **MONEY})
    # await websocket.send(data)
    while(True):
    
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        clientMsg = "Message from Client:{}".format(message)
        clientIP  = "Client IP Address:{}".format(address)
        print(clientMsg)
        print(clientIP)
        if chr(message[0]) == 'E' and chr(message[1]) =='r' and chr(message[2]) == 'r' and chr(message[3]) == 'o' and chr(message[4]) == 'r':
            error_msg = message.decode()
            print(f"Error MSG....{error_msg}")
        elif chr(message[0]) == 'A' and chr(message[1]) =='l' and chr(message[2]) == 'e' and chr(message[3]) == 'r' and chr(message[4]) == 't':
            alert_msg = message.decode()
            print(f"Alert MSG....{alert_msg}")
        elif chr(message[0]) == 'W' and chr(message[1]) =='a' and chr(message[2]) == 'r' and chr(message[3]) == 'n' and chr(message[4]) == 'i':
            warning_msg = message.decode()
            print(f"Warning MSG....{warning_msg}")
        elif chr(message[0]) == 'C' and chr(message[1]) =='r' and chr(message[2]) == 'e' and chr(message[3]) == 'd' and chr(message[4]) == 'i':
            credit_msg = message.decode()
            money = credit_msg.split(':')
            money = money[1]
            money = get_money_value(money)
            MONEY["amount"] = money
            data = json.dumps({"action": "credit", **MONEY})
            put_insert_money(data)
            
            print(f"Credit MSG....{credit_msg} = ${money}")
        elif chr(message[0]) == 'A' and chr(message[1]) =='l' and chr(message[2]) == 'e' and chr(message[3]) == 'r' and chr(message[4]) == 't':
            alert_msg = message.decode()
            print(f"Alert MSG....{alert_msg}")
        elif chr(message[0]) == 'D' and chr(message[1]) =='I' and chr(message[2]) == 'S' and chr(message[3]) == 'A' and chr(message[4]) == 'B':
            # alert_msg = message.decode()
            print("Payout Disable!!!!....")
        elif chr(message[0]) == 'S' and chr(message[1]) =='t' and chr(message[2]) == 'a' and chr(message[3]) == 'c' and chr(message[4]) == 'k':
            alert_msg = message.decode()
            print(f"Alert MSG....{alert_msg}")
        elif chr(message[0]) == 'S' and chr(message[1]) =='t' and chr(message[2]) == 'o' and chr(message[3]) == 'r' and chr(message[4]) == 'e':
            alert_msg = message.decode()
            print(f"Alert MSG....{alert_msg}")
# ReadUDPport()
asyncio.get_event_loop().run_until_complete(ReadUDPport())
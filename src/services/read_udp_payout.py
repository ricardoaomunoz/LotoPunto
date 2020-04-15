import socket 
import time
import asyncio
import json
# import websockets
import sys
sys.path.append("..")
from redis_serv.publish_redis import put_insert_money, put_value_level, put_message, reset_credit
from multiprocessing import Process

readPort = 8080
writePort = 8081
localIP = "127.0.0.1"
bufferSize = 1024


UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

MONEY = {"amount": 0}

def get_money_ch(amount):
    amount = int(amount)
    ch = 0
    if amount == 1000:
        ch = 1
    elif amount == 2000:
        ch = 2
    elif amount == 5000:
        ch = 3
    elif amount == 10000:
        ch = 4
    elif amount == 20000:
        ch = 5
    elif amount == 50000:
        ch = 6
    return ch


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
def WriteUDPport(message):
    msg = str.encode(message)
    UDPServerSocket.sendto(msg, (localIP, int(writePort)))

def get_value_levels():
    for i in range(1,7):
        msg = 'v' + str(i)
        WriteUDPport(msg)
        time.sleep(1)

def set_route(amount, quant):
    ch = get_money_ch(amount)
    print(f"quant: {quant}")
    if quant > 9:
        msg = 'c' + str(ch)
        WriteUDPport(msg)
        put_value_level(ch, "cashbox", quant)
    else:
        msg = 's' + str(ch)
        WriteUDPport(msg)
        put_value_level(ch, "payout", quant)


async def ReadUDPport():
    # uri = "ws://localhost:6789"
    # websocket = websockets.connect(uri)
    # Bind to address and ip
    UDPServerSocket.bind((localIP, readPort))
    print("UDP server up and listening")
    # async with websockets.connect(uri) as websocket:
    # data = json.dumps({"action": "credit", **MONEY})
    # await websocket.send(data)
    # get_value_process = Process(target=get_value_levels)
    reset_credit()
    while(True):
    
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        try:
        
            #Error MSG
            if chr(message[0]) == 'E' and chr(message[1]) =='r' and chr(message[2]) == 'r' and chr(message[3]) == 'o' and chr(message[4]) == 'r':
                error_msg = message.decode()
                print(f"Error MSG....{error_msg}")
                put_message(error_msg, "error")
            #Alert MSG
            elif chr(message[0]) == 'A' and chr(message[1]) =='l' and chr(message[2]) == 'e' and chr(message[3]) == 'r' and chr(message[4]) == 't':
                alert_msg = message.decode()
                print(f"Alert MSG....{alert_msg}")
                put_message(alert_msg, "alert")
            #Warning MSG
            elif chr(message[0]) == 'W' and chr(message[1]) =='a' and chr(message[2]) == 'r' and chr(message[3]) == 'n' and chr(message[4]) == 'i':
                warning_msg = message.decode()
                print(f"Warning MSG....{warning_msg}")
                put_message(warning_msg, "warning")
            #Credit
            elif chr(message[0]) == 'C' and chr(message[1]) =='r' and chr(message[2]) == 'e' and chr(message[3]) == 'd' and chr(message[4]) == 'i':
                credit_msg = message.decode()
                money = credit_msg.split(':')
                money = money[1]
                money = get_money_value(money)
                put_insert_money(money)
                print(f"Credit MSG....{credit_msg} = ${money}")
            #Start
            elif chr(message[0]) == 'S' and chr(message[1]) =='t' and chr(message[2]) == 'a' and chr(message[3]) == 'r' and chr(message[4]) == 't':
                alert_msg = message.decode()
                print(f"MSG....{alert_msg}")
                Process(target=get_value_levels).start()
                # asyncio.get_event_loop().run_until_complete(get_value_levels())
            #Disable
            elif chr(message[0]) == 'D' and chr(message[1]) =='I' and chr(message[2]) == 'S' and chr(message[3]) == 'A' and chr(message[4]) == 'B':
                # alert_msg = message.decode()
                print("Payout Disable!!!!....")
                WriteUDPport('e')
            #Stacked
            elif chr(message[0]) == 'S' and chr(message[1]) =='t' and chr(message[2]) == 'a' and chr(message[3]) == 'c' and chr(message[4]) == 'k':
                alert_msg = message.decode()
                print(f"MSG....{alert_msg}")
                Process(target=get_value_levels).start()
                # asyncio.get_event_loop().run_until_complete(get_value_levels())
            #Stored
            elif chr(message[0]) == 'S' and chr(message[1]) =='t' and chr(message[2]) == 'o' and chr(message[3]) == 'r' and chr(message[4]) == 'e':
                alert_msg = message.decode()
                print(f"MSG....{alert_msg}")
                Process(target=get_value_levels).start()
                # asyncio.get_event_loop().run_until_complete(get_value_levels())
            #Value Level
            elif chr(message[0]) == 'V' and chr(message[1]) =='a' and chr(message[2]) == 'l' and chr(message[3]) == 'u' and chr(message[4]) == 'e':
                alert_msg = message.decode()
                print(f"MSG....{alert_msg}")
                data = alert_msg.split(": ")
                print(f"data.. {data}")
                data = data[1].split(" ")
                print(f"data.. {data}")
                amount = int(data[0])/100
                quantity = int(data[1])
                print(f"quantity: {quantity}")
                set_route(amount, quantity)
            #Dispensed
            elif chr(message[0]) == 'D' and chr(message[1]) =='i' and chr(message[2]) == 's' and chr(message[3]) == 'p' and chr(message[4]) == 'e':
                alert_msg = message.decode()
                print(f"MSG....{alert_msg}")
                Process(target=get_value_levels).start()

        except Exception as err:
            print(f"Error {err} {message}")
            pass
# ReadUPport()
asyncio.get_event_loop().run_until_complete(ReadUDPport())
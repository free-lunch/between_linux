#-*- coding: utf-8 -*-


import sys, os
import threading
import time
import json
import getpass

from lib.client import Client
from lib.bot import Bot

import message_model
from utils import rjust, transColor, getTerminalSize

ID = None
PW = None
client = None
lastest_receive_time = 0
lovers_color = '\033['+'97'+'m' # default : WHITE

"""
Color
Format : \033 + color + m
    Example : '\03397m' (WHITE)
Color Table
    30	Black
    31	Red
    32	Green
    33	Yellow
    34	Blue
    35	Magenta
    36	Cyan
    37	Light gray
    90	Dark gray
    91	Light red
    92	Light green
    93	Light yellow
    94	Light blue
    95	Light magenta
    96	Light cyan
    97	White
"""

def on_message(ws, message):
    global lastest_receive_time
    try:
        msg = message_model.Message(message)
        msg_type = msg.getType()
        if  msg_type == 'MESSAGE':
            msg_id = msg.getValue('id')
            msg_content = msg.getValue('content')
            msg_from = msg.getValue('from')

            client.mark_read_message(msg_id)
            msg_string = msg_content.encode('utf-8')

            if msg_from != client.user_id:
                if time.time() - lastest_receive_time > 60 :
                    os.system('notify-send '+ '\'Receive a message from lover ('\
                    + time.strftime('%H:%M:%S',time.gmtime()) + ')\'')

                lastest_receive_time = time.time()
                print(transColor(rjust(msg_content, screen_width,' '), lovers_color))

        elif msg_type == 'STICKER':
            msg_from = msg.getValue('from')
            msg_sticker_id = msg.getValue('sticker_id')
            if msg_from != client.user_id:
                print(transColor(rjust(msg_sticker_id, screen_width,' '), lovers_color))

        else:
            if msg_type == 'MODIFY':
                msg_from = msg.getValue('from')
                if msg_from != client.user_id:
                    lastest_receive_time = time.time()

    except Exception as e:
        print 'Recving Exception : ', e

def waitTyping(client):
    rl = lambda : sys.stdin.readline()
    while True:
        input_line = rl().rstrip('\n')
        if input_line == "":
            continue
        if input_line == "quit" or input_line == "exit":
            print("==== Success to exit ====")
            break
        client.send(input_line)


if __name__ == '__main__':
    if ID == None:
        ID = raw_input("ID : ")

    if PW == None:
        PW = getpass.getpass("PW : ")

    client = Client(ID,PW)

    sz = getTerminalSize()
    screen_width = sz[0]

    # Print recent messages
    for msg in client.get_recent_messages(15)[::-1]:
        client.mark_read_message(msg.id)
        if hasattr(msg,'content'):
            if msg._from != client.user_id:
                print(transColor(rjust(msg.content, screen_width,' '),lovers_color))
            else:
                print(msg.content)

        else:
            try:
                sticker_id = msg.attachments[0][u'sticker'][u'sticker_id']
                if msg._from != client.user_id:
                    print(transColor(rjust(sticker_id, screen_width,' '),lovers_color))
                else:
                    print(sticker_id)
            except KeyError:
                pass

    print('==== System Message ====')
    print('If you want exit, type exit or quit')
    print('========================')

    t1 = threading.Thread(target=waitTyping, args=(client,))
    bot = Bot(ID,PW, on_message=on_message)
    t2 = threading.Thread(target=bot.run_forever, args=(0.1,))

    t1.start()
    t2.start()
    t1.join()

    bot.__del__()

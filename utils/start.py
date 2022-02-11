
import random
from datetime import datetime
import asyncio

import socks
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import TelegramClient
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import InputChannel
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os, sys
import configparser
import csv
import time
#from data.config import api_id, api_hash
#from loader import scheduler
from baza import select_user_accounts
import os

def cicada():
    api_id = 7265064
    user_id = 1144785510
    api_hash = "9ec54c3437a4b240456f08dd3276f5c3"
    file_list = os.listdir('sessions')
    x = len(file_list)
    i = 1
    while i <= x:
        try:
            acaunt = file_list[i]
            client = TelegramClient(f"sessions/{acaunt}", api_id, api_hash)
            client.connect()
            msg_txt = open('sms.txt', 'r').read()
            client.send_message(user_id, msg_txt, parse_mode="HTML")
            time.sleep(5)
            client.disconnect()
            print(f'     \nОтправленно {i} sms')
            i = i + 1
        except:
            print('     \nРассылка Успешно закоечена')


"""
    client = TelegramClient(f"sessions/{acc[1]}", api_id, api_hash)
        await client.connect()
        msg_txt = 'uhgufuyfu'
        await client.send_message(user_id, msg_txt, parse_mode="HTML")

print(st.)
"""
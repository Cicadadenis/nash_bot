import asyncio
import os
import random
from telethon import TelegramClient, Button, events 
from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import Unauthorized

from keyboards.inline.menu import back_admin, admin_menu, choose_menu
from loader import dp, bot
from states.states import BroadcastState, GiveTime, TakeTime
from utils.db_api.db_commands import select_all_users, del_user, update_date
from calendar import c
from email import message
import random
from telethon.tl.custom import Button
from datetime import datetime
import asyncio
from keyboards.inline.menu import back_to_main_menu,  api_hash, api_id, code_menu, \
    main_menu, proxy_menu, start_spam_menu, accept_spam_menu
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
import random
#from data.config import api_id, api_hash
#from loader import scheduler
import os

from datetime import datetime, timedelta

@dp.callback_query_handler(text="give_time")
async def edit_commission(call: CallbackQuery, state: FSMContext):
    msg_to_edit = await call.message.edit_text("<b>🆔Введите ID человека:</b>",
                                               reply_markup=back_admin)
    await GiveTime.GT1.set()
    await state.update_data(msg_to_edit=msg_to_edit)


@dp.message_handler(state=GiveTime.GT1)
async def receive_com(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit = data.get("msg_to_edit")
    user_id = message.text
    await message.delete()
    await GiveTime.next()
    await state.update_data(user_id=user_id)
    await msg_to_edit.edit_text("<b>⏰Введите время в часах которое выдать человеку:</b>", reply_markup=back_admin)


@dp.message_handler(state=GiveTime.GT2)
async def receive_com(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit, user_id = data.get("msg_to_edit"), data.get("user_id")
    try:
        hours = int(message.text)
        await message.delete()
        date_when_expires = datetime.now() + timedelta(hours=hours)
        date_to_db = str(date_when_expires).split(".")[0].replace("-", " ").split(":")
        date_to_db = " ".join(date_to_db[:-1])
        await update_date(user_id, date_to_db)
        await state.finish()
        await msg_to_edit.edit_text("<b>Доступ выдан.</b>", reply_markup=back_admin)
    except ValueError:
        await msg_to_edit.edit_text("<b>⏰Не верный формат, попробуйте еще раз.</b>")


@dp.callback_query_handler(text="take_time")
async def edit_commission(call: CallbackQuery, state: FSMContext):
    msg_to_edit = await call.message.edit_text("<b>🆔Введите ID человека:</b>",
                                               reply_markup=back_admin)
    await TakeTime.T1.set()
    await state.update_data(msg_to_edit=msg_to_edit)


@dp.message_handler(state=TakeTime.T1)
async def receive_com(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit = data.get("msg_to_edit")
    user_id = message.text
    await message.delete()
    await update_date(user_id, None)
    await state.finish()
    await msg_to_edit.edit_text("<b>У юзера больше нет доступа.</b>", reply_markup=back_admin)


# ========================BROADCAST========================
# ASK FOR PHOTO AND TEXT
@dp.callback_query_handler(text="broadcast")
async def broadcast2(call: CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer("<b>Отправь фото с текстом, которые будут рассылаться по юзерам\n"
                              "Можно просто текст</b>", reply_markup=back_to_main_menu)
    await BroadcastState.BS1.set()


# RECEIVE PHOTO OR TEXT
@dp.message_handler(content_types=['photo', 'text'], state=BroadcastState.BS1)
async def broadcast4(message: Message, state: FSMContext):
    await message.delete()
    if message.photo:
        easy_chars = 'abcdefghijklnopqrstuvwxyz1234567890'
        name = 'cicada'
        photo_name = name + ".jpg"
        await message.photo[-1].download(f"pics/broadcast/{photo_name}")
        await state.update_data(photo=photo_name, text=message.caption)
        await asyncio.sleep(2)
        path = f'pics/broadcast/{photo_name}'
        with open(path, 'rb') as f:
            photo = f.read()
        await message.answer_photo(photo=photo, caption=f"{message.caption}\n\n"
                                                        f"<b>Все правильно? Отправляем?</b>",
                                   reply_markup=choose_menu)
    else:
        await state.update_data(text=message.text)
        await message.answer(message.text + "\n\n<b>Все правильно? Отправляем?</b>", reply_markup=choose_menu)
    await BroadcastState.next()


# START BROADCAST
@dp.callback_query_handler(text="broadcast:yes", state=BroadcastState.BS2)
async def broadcast_text_post(call: CallbackQuery, state: FSMContext):
    users = open('ussers.txt', 'r').readlines()
    data = await state.get_data()
    text, photo_name = data.get("text"), data.get('photo')
    await state.finish()
    msg_to_delete = await call.message.answer("<b>Рассылка начата</b>")
    path = f'pics/broadcast/{photo_name}'
    with open(path, 'rb') as f:
        photo = f.read()
    tt = open('time.txt', 'r')
    ti = int(tt.read())
    tt.close()
    api_id = 7265064
    api_hash = "9ec54c3437a4b240456f08dd3276f5c3"

    
    file_list = os.listdir('sessions')
    xx = len(file_list)
    i = 0
    t = 0
    m = 0
    mx = 40
    a = 0
    msm = 0
    while i <= xx:
        mm = 0
        try:
            file_list = os.listdir('sessions')
            acaunt = file_list[i]
            client = TelegramClient(f"sessions/{acaunt}", api_id, api_hash)
            await client.connect() 
        except:
            await client.disconnect() 
            
        try:
            ss = open('ussers.txt', 'r').readlines()
            z = len(ss)
            count = int(z)
        except:
            await call.message.answer('Список получателей пуст !')
        
        while True:
            try:
                if a <= count:
                    if mm <= 40:
                        try:
                            ssm = open('sms.txt', 'r').read()
                            zz = ssm.split('|')
                            sms = random.choice(zz)
                            ss = open('ussers.txt', 'r').readlines()
                            await client.send_file(ss[a][:-1], file=photo, caption=text)
                            klient = ss[a][:-1]
                            await call.message.edit_text(f"SMS Отправленно пользователю: {klient}")
                            msm = msm + 1
                            mm = mm + 1
                            time.sleep(ti)
                            a = a + 1
                        except:
                            ssm = open('sms.txt', 'r').read()
                            zz = ssm.split('|')
                            sms = random.choice(zz)
                            ss = open('ussers.txt', 'r').readlines()
                            await client.send_message(ss[a][:-1], text)
                            klient = ss[a][:-1]
                            await call.message.edit_text(f"SMS Отправленно пользователю: {klient}")
                            msm = msm + 1
                            mm = mm + 1
                            time.sleep(ti)
                            a = a + 1
                        
                
                    await call.message.answer("Готово беру следующий акаунт")
                    i = i + 1
                await call.message.answer("Готово Все Username Проспамленны")
                i = i + 1
            except:
                await call.message.answer("Готово беру следующий акаунт3")
                i = i + 1


# CANCEL BROADCAST
@dp.callback_query_handler(text="broadcast:no", state=BroadcastState.BS2)
async def broadcast_text_post(call: CallbackQuery, state: FSMContext):
    if not call.message.photo:
        await call.message.edit_text("<b>Админ-меню</b>", reply_markup=admin_menu)
    else:
        await call.message.delete()
        await call.message.answer("<b>Админ-меню</b>", reply_markup=admin_menu)
    await state.finish()

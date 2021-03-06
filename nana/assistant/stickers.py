#
# Settings For Sticker
#
import asyncio
from .settings import get_text_settings, get_button_settings
from pyrogram import filters
from pyrogram.types import ReplyKeyboardMarkup, Message

from nana import setbot, AdminSettings, DB_AVAILABLE, app, Owner, NANA_IMG
from nana.assistant.database.stickers_db import set_sticker_set, set_stanim_set
from nana.assistant.__main__ import dynamic_data_filter

TEMP_KEYBOARD = []
USER_SET = {}
TODEL = {}


@setbot.on_message(filters.user(AdminSettings) & filters.command(["setsticker"]))
async def get_stickers(client, message):
    if not DB_AVAILABLE:
        await message.edit("Your database is not avaiable!")
        return
    global TEMP_KEYBOARD, USER_SET
    await app.send_message("@Stickers", "/stats")
    await asyncio.sleep(0.2)
    keyboard = await app.get_history("@Stickers", limit=1)
    keyboard = keyboard[0].reply_markup.keyboard
    for x in keyboard:
        for y in x:
            TEMP_KEYBOARD.append(y)
    await app.send_message("@Stickers", "/cancel")
    msg = await message.reply("Select your stickers for set as kang sticker",
                              reply_markup=ReplyKeyboardMarkup(keyboard))
    USER_SET[message.from_user.id] = msg.message_id
    USER_SET["type"] = 1

@setbot.on_message(filters.user(AdminSettings) & filters.command(["setanimation"]))
async def get_stickers_animation(client, message):
    if not DB_AVAILABLE:
        await message.edit("Your database is not avaiable!")
        return
    global TEMP_KEYBOARD, USER_SET
    await app.send_message("@Stickers", "/stats")
    await asyncio.sleep(0.2)
    keyboard = await app.get_history("@Stickers", limit=1)
    keyboard = keyboard[0].reply_markup.keyboard
    for x in keyboard:
        for y in x:
            TEMP_KEYBOARD.append(y)
    await app.send_message("@Stickers", "/cancel")
    msg = await message.reply("Select your stickers for set as kang animation sticker",
                              reply_markup=ReplyKeyboardMarkup(keyboard))
    USER_SET[message.from_user.id] = msg.message_id
    USER_SET["type"] = 2

def get_stickerlist(client,message):
    if not DB_AVAILABLE:
        return
    global TEMP_KEYBOARD, USER_SET
    if message.from_user and message.from_user.id in list(USER_SET):
        return True
    else:
        TEMP_KEYBOARD = []
        USER_SET = {}

@setbot.on_message(get_stickerlist)
async def set_stickers(client, message):
    if not DB_AVAILABLE:
        await message.edit("Your database is not avaiable!")
        return
    global TEMP_KEYBOARD, USER_SET
    if message.text in TEMP_KEYBOARD:
        await client.delete_messages(message.chat.id, USER_SET[message.from_user.id])
        if USER_SET["type"] == 1:
            set_sticker_set(message.from_user.id, message.text)
        elif USER_SET["type"] == 2:
            set_stanim_set(message.from_user.id, message.text)
        status = "Ok, sticker was set to `{}`".format(message.text)
    else:
        status = "Invalid pack selected."
    TEMP_KEYBOARD = []
    USER_SET = {}
    text = await get_text_settings()
    text += "\n{}".format(status)
    button = await get_button_settings()
    await setbot.send_photo(message.chat.id, NANA_IMG, caption=text, reply_markup=button)


@setbot.on_callback_query(dynamic_data_filter("setsticker"))
async def settings_sticker(client, message):
    if not DB_AVAILABLE:
        await message.edit("Your database is not avaiable!")
        return
    global TEMP_KEYBOARD, USER_SET
    await app.send_message("@Stickers", "/stats")
    await asyncio.sleep(0.2)
    try:
        keyboard = await app.get_history("@Stickers", limit=1)
        keyboard = keyboard[0].reply_markup.keyboard
    except:
        await message.edit("You dont have any sticker pack!\nAdd stickers pack in @Stickers ")
        return
    for x in keyboard:
        for y in x:
            TEMP_KEYBOARD.append(y)
    await app.send_message("@Stickers", "/cancel")
    await message.message.delete()
    msg = await setbot.send_message(Owner, "Select your stickers for set as kang animation sticker",
                                    reply_markup=ReplyKeyboardMarkup(keyboard))
    USER_SET[message.from_user.id] = msg.message_id
    USER_SET["type"] = 2

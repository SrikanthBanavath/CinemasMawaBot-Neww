# Credit @LazyDeveloper.
# Please Don't remove credit.
# Born to make history @LazyDeveloper !
# Thank you LazyDeveloper for helping us in this Journey
# 🥰  Thank you for giving me credit @LazyDeveloperr  🥰
# for any error please contact me -> telegram@LazyDeveloperr or insta @LazyDeveloperr 
# rip paid developers 🤣 - >> No need to buy paid source code while @LazyDeveloperr is here 😍😍

import asyncio
import re
import ast
import math
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, \
    make_inactive
from info import *
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ForceReply, Message
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results
from database.lazy_utils import progress_for_pyrogram, convert, humanbytes
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import os 
import humanize
from PIL import Image
import time
from utils import get_shortlink
from database.filters_mdb import (
    del_all,
    find_filter,
    get_filters,
)
from util.human_readable import humanbytes
from urllib.parse import quote_plus
from util.file_properties import get_name, get_hash, get_media_file_size
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

cm_search_channel = CM_SEARCH_CHANNEL
req_channel = REQ_CHANNEL
BUTTONS = {}
SPELL_CHECK = {}


@Client.on_message(filters.group & filters.text & filters.incoming)
async def give_filter(client, message):
    k = await manual_filters(client, message)
    if k == False:
        await auto_filter(client, message)

@Client.on_message(filters.private & filters.text & filters.incoming)
async def pv_filter(client, message):
    kd = await manual_filters(client, message)
    if kd == False:
        await auto_filter(client, message)

@Client.on_callback_query(filters.regex('rename'))
async def rename(bot,update):
	user_id = update.message.chat.id
	date = update.message.date
	await update.message.delete()
	await update.message.reply_text("»»——— Please Enter New File Name...",	
	reply_to_message_id=update.message.reply_to_message.id,  
	reply_markup=ForceReply(True))  
# Born to make history @LazyDeveloper !
@Client.on_callback_query(filters.regex("upload"))
async def doc(bot, update):
    type = update.data.split("_")[1]
    new_name = update.message.text
    new_filename = new_name.split(":-")[1]
    file = update.message.reply_to_message
    file_path = f"downloads/{new_filename}"
    ms = await update.message.edit("\n༻☬ད Processing....")
    c_time = time.time()
    try:
        path = await bot.download_media(
                message=file,
                progress=progress_for_pyrogram,
                progress_args=("**\n  ღ♡ File Under Construction... ♡♪**", ms, c_time))
    except Exception as e:
        await ms.edit(e)
        return 
    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name =f"downloads/{dow_file_name}"
    os.rename(old_file_name, file_path)
    duration = 0
    try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
           duration = metadata.get('duration').seconds
    except:
        pass
    user_id = int(update.message.chat.id) 
    ph_path = None 
    media = getattr(file, file.media.value)
    filesize = humanize.naturalsize(media.file_size) 
    c_caption = await db.get_caption(update.message.chat.id)
    c_thumb = await db.get_thumbnail(update.message.chat.id)
    if c_caption:
         try:
             caption = c_caption.format(filename=new_filename, filesize=humanize.naturalsize(media.file_size), duration=convert(duration))
         except Exception as e:
             await ms.edit(text=f"Your caption Error unexpected keyword ●> ({e})")
             return 
    else:
        caption = f"**{new_filename}** \n\n⚡️Data costs: `{filesize}`"
    if (media.thumbs or c_thumb):
        if c_thumb:
           ph_path = await bot.download_media(c_thumb) 
        else:
           ph_path = await bot.download_media(media.thumbs[0].file_id)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")
    await ms.edit("Receiving File...")
    c_time = time.time() 
    try:
       if type == "document":
          await bot.send_document(
	        update.message.chat.id,
                   document=file_path,
                   thumb=ph_path, 
                   caption=caption, 
                   progress=progress_for_pyrogram,
                   progress_args=( "**Receiving File From Server**",  ms, c_time))
       elif type == "video": 
           await bot.send_video(
	        update.message.chat.id,
	        video=file_path,
	        caption=caption,
	        thumb=ph_path,
	        duration=duration,
	        progress=progress_for_pyrogram,
	        progress_args=( "**Receiving File From Server**",  ms, c_time))
       elif type == "audio": 
           await bot.send_audio(
	        update.message.chat.id,
	        audio=file_path,
	        caption=caption,
	        thumb=ph_path,
	        duration=duration,
	        progress=progress_for_pyrogram,
	        progress_args=( "**Receiving File From Server**",  ms, c_time   )) 
    except Exception as e: 
        await ms.edit(f" Erro {e}") 
        os.remove(file_path)
        if ph_path:
          os.remove(ph_path)
        return 
    await ms.delete() 
    os.remove(file_path) 
    if ph_path:
       os.remove(ph_path) 


# Born to make history @LazyDeveloper !
@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):

    ident, req, key, offset = query.data.split("_")
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer("This Message is not for you dear. Don't worry you can send new one !", show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = BUTTONS.get(key)
    if not search:
        await query.answer("You are using one of my old messages, please send the request again.", show_alert=True)
        return

    files, n_offset, total = await get_search_results(search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    settings = await get_settings(query.message.chat.id)
        # if query.from_user.id in download_counts and download_counts[query.from_user.id]['date'] == current_date:
        #     if download_counts[query.from_user.id]['count'] >= DOWNLOAD_LIMIT:
        #         # set URL_MODE to False to disable the URL shortener button
        #         URL_MODE = False
        #     else:
        #         # increment the download count for the user
        #         download_counts[query.from_user.id]['count'] += 1
        # else:
        #     # create a new entry for the user in the download counts dictionary
        #     download_counts[query.from_user.id] = {'date': current_date, 'count': 1}d
    if settings['button']:
            if URL_MODE is True:
                if query.from_user.id in ADMINS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]
                elif query.from_user.id in MY_USERS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]
                elif query.from_user.id in LZURL_PRIME_USERS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                        ]
                elif query.message.chat.id is not None and query.message.chat.id in LAZY_GROUPS:
                    btn = [
                    [
                        InlineKeyboardButton(
                            text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                        ),
                    ]
                    for file in files
                    ]
                else:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", 
                                url=await get_shortlink(f"https://telegram.me/{BOT_USERNAME}?start=files_{file.file_id}")
                            ),
                        ]
                        for file in files
                    ]
            else:
                if query.from_user.id in ADMINS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]
                elif query.from_user.id in MY_USERS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]
                else:    
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]

    else:
        if URL_MODE is True:
                if query.from_user.id in ADMINS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]
                elif query.from_user.id in MY_USERS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]
                elif query.from_user.id in LZURL_PRIME_USERS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                        ]
                elif query.message.chat.id is not None and query.message.chat.id in LAZY_GROUPS:
                    btn = [
                    [
                        InlineKeyboardButton(
                            text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                        ),
                    ]
                    for file in files
                    ]
                else:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", 
                                url=await get_shortlink(f"https://telegram.me/{BOT_USERNAME}?start=files_{file.file_id}")
                            ),
                        ]
                        for file in files
                    ]
        else:
                if query.from_user.id in ADMINS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]
                elif query.from_user.id in MY_USERS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]
                else:    
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]


    if 0 < offset <= 10:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - 10
    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("⏪ BACK", callback_data=f"next_{req}_{key}_{off_set}"),
             InlineKeyboardButton(f"📃 Pages {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}",
                                  callback_data="pages")]
        )
    elif off_set is None:
        btn.append(
            [InlineKeyboardButton(f"🗓 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}", callback_data="pages"),
             InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{req}_{key}_{n_offset}")])
    else:
        btn.append(
            [
                InlineKeyboardButton("⏪ BACK", callback_data=f"next_{req}_{key}_{off_set}"),
                InlineKeyboardButton(f"🗓 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}", callback_data="pages"),
                InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{req}_{key}_{n_offset}")
            ],
        )
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()


@Client.on_callback_query(filters.regex(r"^spol"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("This Message is not for you dear. Don't worry you can send new one !", show_alert=True)
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movies = SPELL_CHECK.get(query.message.reply_to_message.id)
    if not movies:
        return await query.answer("You are clicking on an old button which is expired.", show_alert=True)
    movie = movies[(int(movie_))]
    await query.answer('Checking for Movie in database...')
    files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
    if files:
        k = (movie, files, offset, total_results)
        await auto_filter(bot, query, k)
    else:
        k = await query.message.edit('<b>Hey Dear, \nThe Requested Content is Currently Not Available in My Database. Have Some Patience 🙂 - Our great admin will upload it as soon as possible </b>')
        await asyncio.sleep(10)
        await k.delete()


# Born to make history @LazyDeveloper !
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    data = query.data
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Make sure I'm present in your group!!", quote=True)
            else:
                await query.message.edit_text(
                    "I'm not connected to any groups!\nCheck /connections or connect to any groups",
                    quote=True
                )

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return await query.answer('Piracy is Crime!')

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("You need to be Group Owner or an Auth User to do that!", show_alert=True)
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("That's not for you Dear!", show_alert=True)
    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("DELETE", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("BACK", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Group Name : **{title}**\nGroup ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN
        )
    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Connected to **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text('Some error occurred!!', parse_mode=enums.ParseMode.MARKDOWN)
    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Successfully deleted connection"
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)

    if query.data.startswith("file"):
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        settings = await get_settings(query.message.chat.id)
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"

        try:
            if (AUTH_CHANNEL or JOIN_REQ_CHANNEL) and not await is_subscribed(client, query):
                if clicked == typed:
                    await query.answer(url=f"https://t.me/{BOT_USERNAME}?start={ident}_{file_id}")
                    return
                else:
                    await query.answer(f"𝖧𝖾𝗒 {query.from_user.first_name}, 𝖳𝗁𝗂𝗌 𝗂𝗌 𝗇𝗈𝗍 𝗒𝗈𝗎𝗋 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 !", show_alert=True)
            elif settings['botpm']:
                if clicked == typed:
                    await query.answer(url=f"https://t.me/{BOT_USERNAME}?start={ident}_{file_id}")
                    return
                else:
                    await query.answer(f"𝖧𝖾𝗒 {query.from_user.first_name}, 𝖳𝗁𝗂𝗌 𝗂𝗌 𝗇𝗈𝗍 𝗒𝗈𝗎𝗋 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 !", show_alert=True)
            else:
                if clicked == typed:
                    await client.send_cached_media(
                        chat_id=query.from_user.id,
                        file_id=file_id,
                        caption=f_caption,
                        protect_content=True if ident == "filep" else False,
                        reply_markup=InlineKeyboardMarkup( [] ))
                else:
                    await query.answer(f"𝖧𝖾𝗒 {query.from_user.first_name}, 𝖳𝗁𝗂𝗌 𝗂𝗌 𝗇𝗈𝗍 𝗒𝗈𝗎𝗋 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 !", show_alert=True)
                await query.answer('𝖢𝗁𝖾𝖼𝗄 𝖯𝖬, 𝖨 𝗁𝖺𝗏𝖾 𝗌𝖾𝗇𝗍 𝖿𝗂𝗅𝖾𝗌 𝗂𝗇 𝖯𝖬', show_alert=True)
        except UserIsBlocked:
            await query.answer('𝖴𝗇𝖻𝗅𝗈𝖼𝗄 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗆𝖺𝗇𝗁 !', show_alert=True)
        except PeerIdInvalid:
            await query.answer(url=f"https://t.me/{BOT_USERNAME}?start={ident}_{file_id}")
        except Exception as e:
            await query.answer(url=f"https://t.me/{BOT_USERNAME}?start={ident}_{file_id}")

    elif query.data.startswith("checksub"):
        if (AUTH_CHANNEL or JOIN_REQ_CHANNEL) and not await is_subscribed(client, query):
            await query.answer("𝙸 𝙻𝚒𝚔𝚎 𝚈𝚘𝚞𝚛 𝚂𝚖𝚊𝚛𝚝𝚗𝚎𝚜𝚜, 𝙱𝚞𝚝 𝙳𝚘𝚗'𝚝 𝙱𝚎 𝙾𝚟𝚎𝚛𝚜𝚖𝚊𝚛𝚝 𝙾𝚔𝚊𝚢 😉", show_alert=True)
            return
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
                f_caption = f_caption
        if f_caption is None:
            f_caption = f"{title}"
        await query.answer()
        # Create the inline keyboard button with callback_data
        button = InlineKeyboardButton('🖥Watch Online / Fast Download⚡️', callback_data=f'generate_stream_link:{file_id}')
            
        # Create the inline keyboard markup with the button
        keyboard = InlineKeyboardMarkup([[button]])
        await client.send_cached_media(
            chat_id=query.from_user.id,
            file_id=file_id,
            caption=f_caption,
            reply_markup=keyboard,
            protect_content=True if ident == 'checksubp' else False
        )
	
    elif query.data == "pages":
        await query.answer()
    elif query.data == "start":
        buttons = [[
            InlineKeyboardButton("➕️ Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ ➕", url=f"http://t.me/{BOT_USERNAME}?startgroup=true")
            ],[
            InlineKeyboardButton("Sᴇᴀʀᴄʜ 🔎", switch_inline_query_current_chat=''), 
            InlineKeyboardButton("Uᴘᴅᴀᴛᴇs 🔈", url="https://t.me/+n8l5UcES7IE3MmU1")
            ],[      
            InlineKeyboardButton("Hᴇʟᴩ 🕸️", callback_data="help"),
            InlineKeyboardButton("Aʙᴏᴜᴛ ✨", callback_data="about")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )


        #await query.answer('♥️ Thank You LazyDeveloper ♥️')
    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('Mᴀɴᴜᴀʟ Fɪʟᴛᴇʀ', callback_data='manuelfilter'),
            InlineKeyboardButton('Aᴜᴛᴏ Fɪʟᴛᴇʀ', callback_data='autofilter')
        ], [
            InlineKeyboardButton('Cᴏɴɴᴇᴄᴛɪᴏɴ', callback_data='coct'),
            InlineKeyboardButton('Exᴛʀᴀ Mᴏᴅs', callback_data='extra')
        ], [
            InlineKeyboardButton('🏠 Hᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('🦠 Sᴛᴀᴛᴜs', callback_data='stats')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "about":
        buttons = [[
            InlineKeyboardButton('🏠 Hᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('🔐 Cʟᴏsᴇ', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "source":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Bᴀᴄᴋ', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.SOURCE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "manuelfilter":
        buttons = [[
            InlineKeyboardButton('🚪 Bᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('⏹️ Bᴜᴛᴛᴏɴs', callback_data='button')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.MANUELFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "button":
        buttons = [[
            InlineKeyboardButton('🚪 Bᴀᴄᴋ', callback_data='manuelfilter')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.BUTTON_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "autofilter":
        buttons = [[
            InlineKeyboardButton('🚪 Bᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.AUTOFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )


    elif data.startswith("generate_stream_link"):
        _, file_id = data.split(":")
        try:
            user_id = query.from_user.id
            username =  query.from_user.mention 

            log_msg = await client.send_cached_media(
                chat_id=LOG_CHANNEL,
                file_id=file_id,
            )
            fileName = get_name(log_msg)
            #fileName = {quote_plus(get_name(log_msg))}
            lazy_stream = f"{URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
            lazy_download = f"{URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"

            xo = await query.message.reply_text(f'<code>Please Wait...</code>')
            await asyncio.sleep(1)
            await xo.delete()

            await log_msg.reply_text(
                text=f"•• Link Generated For #{user_id} \n\n•• UserName : {username} \n\n•• FileName : {fileName}",
                quote=True,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🖥𝗪𝗮𝘁𝗰𝗵 𝗢𝗻𝗹𝗶𝗻𝗲", url=lazy_stream),  # we download Link
                                                    InlineKeyboardButton('𝗙𝗮𝘀𝘁 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱⚡️', url=lazy_download)]])  # web stream Link
            )
            await query.message.reply_text(
                text="<b>Link Generated⚡️</b>",
                quote=True,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🖥𝗪𝗮𝘁𝗰𝗵 𝗢𝗻𝗹𝗶𝗻𝗲", url=lazy_stream),  # we download Link
                                                    InlineKeyboardButton('𝗙𝗮𝘀𝘁 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱⚡️', url=lazy_download)]])  # web stream Link
            )
        except Exception as e:
            print(e)  # print the error message
            await query.answer(f"Something Went Wrong Baby!\n\n{e}", show_alert=True)
            return


    elif data.startswith("notify_user_not_avail"):
        _, user_id, movie = data.split(":")
        # Send message to user
        try:
            btn = [[
                InlineKeyboardButton(text=f"🔍 Search Here 🔎", url="https://t.me/CinemasMawaDiscussion")
            ],[
                InlineKeyboardButton(text=f" Report Issue ⚠️", url=f"https://t.me/Srikanth_Official_Bot")
            ]]
            btn_lzdv = [
                [
                InlineKeyboardButton(text=f"🗑 Delete Log ❌", callback_data = "close_data")
                ]]
            reply_markup_lzdv = InlineKeyboardMarkup(btn_lzdv)
            reply_markup = InlineKeyboardMarkup(btn)
            await client.send_message(int(user_id), f"😒 Oops! Dear, \nYour requested content named  '<b>{movie}</b>'  is not Released In OTT \n\nBut You Can Get This Movie by Searching In Our Group By Another Bot \n\n❤ Thank You for Supporting us.", reply_markup=reply_markup)
            await query.edit_message_text(text=f"- __**User notified successfully...✅**__\n\n⏳**Status** : Not Available 😒.\n🪪**UserID** : `{user_id}`\n🎞**Content** : `{movie}`\n\n\n🦋",reply_markup=reply_markup_lzdv)
        # Delete callback query message
            await query.answer()
            await query.delete()
        except Exception as e:
            print(e)  # print the error message
            await query.answer(f"Something Went Wrong Baby!\n\n{e}", show_alert=True)
            return
        
    elif data.startswith("notify_user_alrupl"):
        _, user_id, movie = data.split(":")
        # Send message to user
        try:
            btn = [[
                InlineKeyboardButton(text=f"🔍 Search Here 🔎", url="https://t.me/CinemasMawaDiscussion")
            ],[
                InlineKeyboardButton(text=f" Report Issue ⚠️", url=f"https://t.me/Srikanth_Official_Bot")
            ]]
            btn_lzdv = [
                [
                InlineKeyboardButton(text=f"🗑 Delete Log ❌", callback_data = "close_data")
                ]]
            reply_markup_lzdv = InlineKeyboardMarkup(btn_lzdv)            
            reply_markup = InlineKeyboardMarkup(btn)
            await client.send_message(int(user_id), f"Hey Dear, \nINVALID SEARCH  '<b>{movie}</b>'  \n\n● For Movies Type Movie Name with Year \nEx : Kantara 2022. \n\n● For Series Just Type Series Name With Season Number \nEx : Peaky Blinders S01\n   Breaking Bad S05...\n\n❤ Thank You for Supporting us", reply_markup=reply_markup)
            await query.edit_message_text(text=f"- __**User notified successfully...✅**__\n\n⏳**Status** : Invalid Search ⚡.\n🪪**UserID** : `{user_id}`\n🎞**Content** : `{movie}`\n\n\n🦋",reply_markup=reply_markup_lzdv)
        # Delete callback query message
            await query.answer()
            await query.delete()
        except Exception as e:
            print(e)  # print the error message
            await query.answer(f"Something Went Wrong Baby!\n\n{e}", show_alert=True)
            return
        
    elif data.startswith("notify_userupl"):
        _, user_id, movie = data.split(":")
        # Send message to user
        try:
            btn = [[
                InlineKeyboardButton(text=f"🔍 Search Here 🔎", url="https://t.me/CinemasMawaDiscussion")
            ],[
                InlineKeyboardButton(text=f" Report Issue ⚠️", url=f"https://t.me/Srikanth_Official_Bot")
            ]]
            btn_lzdv = [
                [
                InlineKeyboardButton(text=f"🗑 Delete Log ❌", callback_data = "close_data")
                ]]
            reply_markup_lzdv = InlineKeyboardMarkup(btn_lzdv) 
            reply_markup = InlineKeyboardMarkup(btn)
            await client.send_message(int(user_id), f"✅ Hey Dear, \nYour requested content named  '<b>{movie}</b>'  is now available in our database! You can easily get this movie by searching it's correct name in our official group...\n\n❤ Thank You for Supporting us", reply_markup=reply_markup)
            await query.edit_message_text(text=f"- __**User notified successfully...✅**__\n\n⏳**Status** : Upload done ✅.\n🪪**UserID** : `{user_id}`\n🎞**Content** : `{movie}`\n\n\n🦋", reply_markup=reply_markup_lzdv)
        # Delete callback query message
            await query.answer()
            await query.delete()
        except Exception as e:
            print(e)  # print the error message
            await query.answer(f"Something Went Wrong Baby!\n\n{e}", show_alert=True)
            return
        
    elif data.startswith("notify_user_req_rejected"):
        _, user_id, movie = data.split(":")
        # Send message to user
        try:
            btn = [[
                InlineKeyboardButton(text=f"🔍 Search Here 🔎", url="https://t.me/CinemasMawaDiscussion")
            ],[
                InlineKeyboardButton(text=f" Report Issue ⚠️", url=f"https://t.me/Srikanth_Official_Bot")
            ]]
            btn_lzdv = [
                [
                InlineKeyboardButton(text=f"🗑 Delete Log ❌", callback_data = "close_data")
                ]]
            reply_markup_lzdv = InlineKeyboardMarkup(btn_lzdv) 
            reply_markup = InlineKeyboardMarkup(btn)
            await client.send_message(int(user_id), f"🙇‍♀️ Sorry Dear! \nYour requested content named  '<b>{movie}</b>'  is rejected by our **ADMiN**, we are really very sorry for the inconvenience, we can't process your request at the moment...\n\n❤️‍🩹Keep your search environment friendly, sweetheart!", reply_markup=reply_markup)
            await query.edit_message_text(text=f"- __**User notified successfully...✅**__\n\n⏳**Status** : Request Rejected ❌.\n🪪**UserID** : `{user_id}`\n🎞**Content** : `{movie}`\n\n\n🦋",reply_markup=reply_markup_lzdv)
        # Delete callback query message
            await query.answer()
            await query.delete()
        except Exception as e:
            print(e)  # print the error message
            await query.answer(f"Something Went Wrong Baby!\n\n{e}", show_alert=True)
            return
        
    elif data.startswith("notify_user_spelling_error"):
        _, user_id, movie = data.split(":")
        # Send message to user
        try:
            btn = [[
                InlineKeyboardButton(text=f"🔍 Search Here 🔎", url="https://t.me/CinemasMawaDiscussion")
            ],[
                InlineKeyboardButton(text=f" Report Issue ⚠️", url=f"https://t.me/Srikanth_Official_Bot")
            ]]
            btn_lzdv = [
                [
                InlineKeyboardButton(text=f"🗑 Delete Log ❌", callback_data = "close_data")
                ]]
            reply_markup_lzdv = InlineKeyboardMarkup(btn_lzdv) 
            reply_markup = InlineKeyboardMarkup(btn)
            await client.send_message(int(user_id), f"🌍 Your spelling matters.\nThe requested content  '<b>{movie}</b>'  is available in our database, You were unable to get it because of your spelling mistake.🧐 Please make sure you've spelled correctly while searching content in group...\n\n❤Thank u for supporting us..", reply_markup=reply_markup)
            await query.edit_message_text(text=f"- __**User notified successfully...✅**__\n\n⏳**Status** : Spelling error 🖊.\n🪪**UserID** : `{user_id}`\n🎞**Content** : `{movie}`\n\n\n🦋",reply_markup=reply_markup_lzdv)
        # Delete callback query message
            await query.answer()
            await query.delete()
        except Exception as e:
            print(e)  # print the error message
            await query.answer(f"Something Went Wrong Baby!\n\n{e}", show_alert=True)
            return
        
    elif data.startswith("notify_user_custom"):
        _, user_id, movie = data.split(":")
        # Send message to user
        try:
            btn = [[
                InlineKeyboardButton(text=f"🔍 Search Here 🔎", url="https://t.me/CinemasMawaDiscussion")
            ],[
                InlineKeyboardButton(text=f" Report Issue ⚠️", url=f"https://t.me/Srikanth_Official_Bot")
            ]]
            btn_lzdv = [
                [
                InlineKeyboardButton(text=f"🗑 Delete Log ❌", callback_data = "close_data")
                ]]
            reply_markup_lzdv = InlineKeyboardMarkup(btn_lzdv) 
            reply_markup = InlineKeyboardMarkup(btn)
            await client.send_message(int(user_id), f"🌍 Your spelling matters.\nThe requested content `{movie}` is available in our database, You were unable to get it because of your spelling mistake.🧐 Please make sure you've spelled correctly while searching content in group...\n\n❤Thank u for supporting us.", reply_markup=reply_markup)
            await query.edit_message_text(text=f"- __**User notified successfully...✅**__\n\n⏳**Status** : Spelling error 🖊.\n🪪**UserID** : `{user_id}`\n🎞**Content** : `{movie}`\n\n\n🦋",reply_markup=reply_markup_lzdv)
        # Delete callback query message
            await query.answer()
            await query.delete()
        except Exception as e:
            print(e)  # print the error message
            await query.answer(f"Something Went Wrong Baby!\n\n{e}", show_alert=True)
            return
        
    elif data.startswith("notify_user_req_rcvd"):
        _, user_id, movie = data.split(":")
        # Send message to user
        try:
            btn = [[
                InlineKeyboardButton(text=f"💛 Request More 💛", url=f"https://telegram.me/{MOVIE_GROUP_USERNAME}")
            ],[
                InlineKeyboardButton(text=f" Report Issue ⚠️", url=f"https://t.me/Srikanth_Official_Bot")
            ]]
            btn_lzdv = [
                        [InlineKeyboardButton(text=f"♻ ̶R̶e̶q̶u̶e̶s̶t̶ ̶R̶e̶c̶i̶e̶v̶e̶d ♻", callback_data=f"notify_user_req_rcvd:{user_id}:{movie}")],
                        [InlineKeyboardButton(text=f"✅UPLOAD DONE", callback_data=f"notify_userupl:{user_id}:{movie}")],
                        [InlineKeyboardButton(text=f"⚡INVALID", callback_data=f"notify_user_alrupl:{user_id}:{movie}"),InlineKeyboardButton("🖊SPELL ERROR", callback_data=f"notify_user_spelling_error:{user_id}:{movie}")],
                        [InlineKeyboardButton(text=f"😒NO OTT", callback_data=f"notify_user_not_avail:{user_id}:{movie}"),InlineKeyboardButton("❌Reject Req", callback_data=f"notify_user_req_rejected:{user_id}:{movie}")]
                       ]
            reply_markup_lzdv = InlineKeyboardMarkup(btn_lzdv) 
            reply_markup = InlineKeyboardMarkup(btn)
            await client.send_message(int(user_id), f"💞Hello sweetheart ! we have recieved your request for  `{movie}`... \n\nPlease keep some patience, we will upload it as soon as possible. \n❤ Thank u for your Love .❤", reply_markup=reply_markup)
            await query.edit_message_text(text=f"- __**User notified successfully sweetie...✅**__\n\n⏳**Status** : Request Recieved 🖊.\n🪪**UserID** : `{user_id}`\n🎞**Content** : `{movie}`\n\n\n🦋",reply_markup=reply_markup_lzdv)
        # Delete callback query message
            await query.answer()
            await query.delete()
        except Exception as e:
            print(e)  # print the error message
            await query.answer(f"Something Went Wrong Baby!\n\n{e}", show_alert=True)
            return
        
    elif query.data == "coct":
        buttons = [[
            InlineKeyboardButton('🚪 Bᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CONNECTION_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "extra":
        buttons = [[
            InlineKeyboardButton('🚪 Bᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('👑 Aᴅᴍɪɴ', callback_data='admin')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.EXTRAMOD_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "admin":
        buttons = [[
            InlineKeyboardButton('🚪 Bᴀᴄᴋ', callback_data='extra')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ADMIN_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "stats":
        buttons = [[
            InlineKeyboardButton('🚪 Bᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('♻️ Rᴇғʀᴇsʜ', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    # elif query.data == "getlazythumbnail":
    #     buttons = [
    #         [
    #         InlineKeyboardButton("D͢o͢n͢a͢t͢e͢ L͢a͢z͢y͢D͢e͢v͢", callback_data="thdonatelazydev"),
    #         ],
    #         [ InlineKeyboardButton("<- G̳O̳ ̳B̳A̳C̳K̳  ⨳", callback_data="lazyhome") ]
    #         ]
    #     reply_markup = InlineKeyboardMarkup(buttons)
    #     await query.message.edit_text(
    #         text=script.LZTHMB_TEXT.format(query.from_user.mention),
    #         reply_markup=reply_markup,
    #         parse_mode=enums.ParseMode.HTML
    #     )
    # elif query.data == "thdonatelazydev":
    #     buttons = [
    #         [ InlineKeyboardButton("<- G̳O̳ ̳B̳A̳C̳K̳  ⨳", callback_data="getlazythumbnail") ]
    #         ]
    #     reply_markup = InlineKeyboardMarkup(buttons)
    #     await query.message.edit_text(
    #         text=script.DNT_TEXT.format(query.from_user.mention),
    #         reply_markup=reply_markup,
    #         parse_mode=enums.ParseMode.HTML
    #     )
    # elif query.data == "getlazylink":
    #     buttons = [
    #         [
    #         InlineKeyboardButton("D͢o͢n͢a͢t͢e͢ L͢a͢z͢y͢D͢e͢v͢", callback_data="linkdonatelazydev"),
    #         ],
    #         [ InlineKeyboardButton("<- G̳O̳ ̳B̳A̳C̳K̳  ⨳", callback_data="lazyhome") ]
    #         ]
    #     reply_markup = InlineKeyboardMarkup(buttons)
    #     await query.message.edit_text(
    #         text=script.LZLINK_TEXT.format(query.from_user.mention),
    #         reply_markup=reply_markup,
    #         parse_mode=enums.ParseMode.HTML
    #     )
    elif query.data == "donatelazydev":
        buttons = [
            [ InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close_data") ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.DNT_TEXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "lazyhome":
        text = f"""**Please tell, what should i do with this file.?**\n"""
        buttons = [[ InlineKeyboardButton("📝𝚂𝚃𝙰𝚁𝚃 𝚁𝙴𝙽𝙰𝙼𝙴📝", callback_data="rename") ],
                           [ InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="cancel") ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
                    text=text,
                    reply_markup=reply_markup,
                    parse_mode=enums.ParseMode.HTML
                )    
    elif query.data == "requireauth":
        buttons = [
            [ InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="cancel") ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.REQ_AUTH_TEXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    # elif query.data == "reqauthgetlazythumbnail":
    #     buttons = [
    #         [
    #         InlineKeyboardButton("D͢o͢n͢a͢t͢e͢ L͢a͢z͢y͢D͢e͢v͢", callback_data="thdonatelazydev"),
    #         ],
    #         [ InlineKeyboardButton("<- G̳O̳ ̳B̳A̳C̳K̳  ⨳", callback_data="reqauthlazyhome") ]
    #         ]
    #     reply_markup = InlineKeyboardMarkup(buttons)
    #     await query.message.edit_text(
    #         text=script.LZTHMB_TEXT.format(query.from_user.mention),
    #         reply_markup=reply_markup,
    #         parse_mode=enums.ParseMode.HTML
    #     )
    # elif query.data == "reqauthlazyhome":
    #     text = f"""\n⨳ *•.¸♡ L҉ΛＺ𝐲 ＭⓄｄ𝓔 ♡¸.•* ⨳\n\n**Please tell, what should i do with this file.?**\n"""
    #     buttons = [[ InlineKeyboardButton("📝✧✧ S𝚝ar𝚝 re𝚗aᗰi𝚗g ✧✧📝", callback_data="requireauth") ],
    #                        [ InlineKeyboardButton("⨳  C L Ф S Ξ  ⨳", callback_data="cancel") ]]
    #     reply_markup = InlineKeyboardMarkup(buttons)
    #     await query.message.edit_text(
    #                 text=text,
    #                 reply_markup=reply_markup,
    #                 parse_mode=enums.ParseMode.HTML
    #             )
    # elif query.data == "reqauthgetlazylink":
    #     buttons = [
    #         [
    #         InlineKeyboardButton("D͢o͢n͢a͢t͢e͢ L͢a͢z͢y͢D͢e͢v͢", callback_data="linkdonatelazydev"),
    #         ],
    #         [ InlineKeyboardButton("<- G̳O̳ ̳B̳A̳C̳K̳  ⨳", callback_data="reqauthlazyhome") ]
    #         ]
    #     reply_markup = InlineKeyboardMarkup(buttons)
    #     await query.message.edit_text(
    #         text=script.LZLINK_TEXT.format(query.from_user.mention),
    #         reply_markup=reply_markup,
    #         parse_mode=enums.ParseMode.HTML
    #     )
    elif query.data == "exit":
        await query.answer("Sorry Darling! You can't make any changes...\n\nOnly my Admin can change this setting...", show_alert = True)
        return
    elif query.data == "invalid_index_process":
        await query.answer("Hey sweetie, please send me the last media with quote from your group.\nAnd also make sure that i am admin in your beloved group...")
        return
    # elif query.data == "already_uploaded":
    #     if query.from_user.id not in ADMINS:
    #         await query.answer("Sorry Darling! You can't make any changes...\n\nOnly my Admin can change this setting...", show_alert = True)
    #         return
    #     else:
    #         message = message.text
    #         chat_id = message.chat_id
    #         extracted_line = re.search(pattern, message, re.MULTILINE)
    #         if extracted_line:
    #           # Send the extracted line to the other group chat
    #             buttons = [
    #             [ InlineKeyboardButton("⨳ ok ⨳", callback_data="cancel") ]
    #             ]
    #             reply_markup = InlineKeyboardMarkup(buttons)
    #             await client.send_message(MOVIE_GROUP_ID, text=extracted_line.group(1))
    elif query.data == "cancel":
        try:
            await query.message.delete()
        except:
            return
    elif query.data == "rfrsh":
        await query.answer("Fetching MongoDb DataBase")
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Bᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('♻️ Rᴇғʀᴇsʜ', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        grpid = await active_connection(str(query.from_user.id))

        if str(grp_id) != str(grpid):
            await query.message.edit("Your Active Connection Has Been Changed. Go To /settings.")

        if status == "True":
            await save_group_settings(grpid, set_type, False)
        else:
            await save_group_settings(grpid, set_type, True)

        settings = await get_settings(grpid)

        if settings is not None:
            if query.from_user.id in ADMINS:
                buttons = [
                [
                    InlineKeyboardButton('Filter Button',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Single' if settings["button"] else 'Double',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Bot PM', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["botpm"] else '❌ No',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('File Secure',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["file_secure"] else '❌ No',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('IMDB', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["imdb"] else '❌ No',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Spell Check',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["spell_check"] else '❌ No',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Welcome', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["welcome"] else '❌ No',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ]
            ]
            else:
                buttons = [
                [
                    InlineKeyboardButton('Filter Button',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Single' if settings["button"] else 'Double',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Bot PM', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["botpm"] else '❌ No',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('File Secure',
                                         callback_data=f'exit'),
                    InlineKeyboardButton('✅ Yes' if settings["file_secure"] else '❌ No',
                                         callback_data=f'exit')
                ],
                [
                    InlineKeyboardButton('IMDB', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["imdb"] else '❌ No',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Spell Check',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["spell_check"] else '❌ No',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Welcome', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["welcome"] else '❌ No',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_reply_markup(reply_markup)

async def auto_filter(client, msg, spoll=False):
    if not spoll:
        message = msg
        settings = await get_settings(message.chat.id)
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if 2 < len(message.text) < 100:
            search = message.text
            requested_movie = search.strip()
            user_id = message.from_user.id
            files, offset, total_results = await get_search_results(search.lower(), offset=0, filter=True)
            if not files:
                await client.send_message(req_channel,f"🦋 **REQUESTED CONTENT** 🦋-\n\n**Content Name** :`{search}`\n**Requested By**: {message.from_user.mention}\n **USER ID**:{user_id}\n\n🗃️",
                                                                                                       reply_markup=InlineKeyboardMarkup([
                                                                                                                                        [InlineKeyboardButton(text=f"🤞Request Recieved", callback_data=f"notify_user_req_rcvd:{user_id}:{requested_movie}")],
                                                                                                                                        [InlineKeyboardButton(text=f"✅Upload Done", callback_data=f"notify_userupl:{user_id}:{requested_movie}")],
                                                                                                                                        [InlineKeyboardButton(text=f"⚡INVALID..", callback_data=f"notify_user_alrupl:{user_id}:{requested_movie}"),InlineKeyboardButton("🖊Spell Error", callback_data=f"notify_user_spelling_error:{user_id}:{requested_movie}")],
                                                                                                                                        [InlineKeyboardButton(text=f"😒No OTT", callback_data=f"notify_user_not_avail:{user_id}:{requested_movie}"),InlineKeyboardButton("❌Reject Req", callback_data=f"notify_user_req_rejected:{user_id}:{requested_movie}")],
                                                                                                                                        ]))
                return await advantage_spell_chok(client, msg)

        else: 
            return
    else:
        settings = await get_settings(msg.message.chat.id)
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = spoll
    pre = 'filep' if settings['file_secure'] else 'file'
    if settings["button"]:
            if URL_MODE is True:
                if message.from_user.id in ADMINS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]
                elif message.from_user.id in MY_USERS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]
                elif message.from_user.id in LZURL_PRIME_USERS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'{pre}#{file.file_id}'
                            ),
                        ]
                        for file in files
                        ]
                elif message.chat.id is not None and message.chat.id in LAZY_GROUPS:
                    btn = [
                    [
                        InlineKeyboardButton(
                            text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'{pre}#{file.file_id}'
                        ),
                    ]
                    for file in files
                    ]
                else:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", 
                                url=await get_shortlink(f"https://telegram.me/{BOT_USERNAME}?start=files_{file.file_id}")
                            ),
                        ]
                        for file in files
                    ]
            else:
                if message.from_user.id in ADMINS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]
                elif message.from_user.id in MY_USERS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]
                else:    
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'{pre}#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]

    else:
        if URL_MODE is True:
                if message.from_user.id in ADMINS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]
                elif message.from_user.id in MY_USERS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]
                elif message.from_user.id in LZURL_PRIME_USERS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'{pre}#{file.file_id}'
                            ),
                        ]
                        for file in files
                        ]
                elif message.chat.id is not None and message.chat.id in LAZY_GROUPS:
                    btn = [
                    [
                        InlineKeyboardButton(
                            text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'{pre}#{file.file_id}'
                        ),
                    ]
                    for file in files
                    ]
                else:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", 
                                url=await get_shortlink(f"https://telegram.me/{BOT_USERNAME}?start=files_{file.file_id}")
                            ),
                        ]
                        for file in files
                    ]
        else:
                if message.from_user.id in ADMINS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]
                elif message.from_user.id in MY_USERS:
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]
                else:    
                    btn = [
                        [
                            InlineKeyboardButton(
                                text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'{pre}#{file.file_id}'
                            ),
                        ]
                        for file in files
                    ]

	
    if offset != "":
        key = f"{message.chat.id}-{message.id}"
        BUTTONS[key] = search
        req = message.from_user.id if message.from_user else 0
        btn.append(
            [InlineKeyboardButton(text=f"🗓 1/{math.ceil(int(total_results) / 10)}", callback_data="pages"),
             InlineKeyboardButton(text="NEXT ⏩", callback_data=f"next_{req}_{key}_{offset}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton(text="🗓 1/1", callback_data="pages")]
        )

    search = message.text

    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    TEMPLATE = settings['template']
    # waiting overs here @LazyDeveloperr

    if imdb:
        cap = TEMPLATE.format(
            query=search,
            title=imdb['title'],
            votes=imdb['votes'],
            aka=imdb["aka"],
            seasons=imdb["seasons"],
            box_office=imdb['box_office'],
            localized_title=imdb['localized_title'],
            kind=imdb['kind'],
            imdb_id=imdb["imdb_id"],
            cast=imdb["cast"],
            runtime=imdb["runtime"],
            countries=imdb["countries"],
            certificates=imdb["certificates"],
            languages=imdb["languages"],
            director=imdb["director"],
            writer=imdb["writer"],
            producer=imdb["producer"],
            composer=imdb["composer"],
            cinematographer=imdb["cinematographer"],
            music_team=imdb["music_team"],
            distributors=imdb["distributors"],
            release_date=imdb['release_date'],
            year=imdb['year'],
            genres=imdb['genres'],
            poster=imdb['poster'],
            plot=imdb['plot'],
            rating=imdb['rating'],
            url=imdb['url'],
            **locals()
        )
    else:
        await client.send_message(cm_search_channel,f"Search : {search}\nUser : {message.from_user.mention}\nUser ID : {user_id}"),
        cap = f"⚡Baby, Here is what i found for your query <code>{search}</code>"
    if imdb and imdb.get('poster'):
        try:
            z = await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024],
                                        reply_markup=InlineKeyboardMarkup(btn))
            if SELF_DELETE:
                await asyncio.sleep(SELF_DELETE_SECONDS)
                await z.delete()
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")

            m = await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
            if SELF_DELETE:
                await asyncio.sleep(SELF_DELETE_SECONDS)
                await m.delete()
                                          
        except Exception as e:
            logger.exception(e)
            n = await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
            if SELF_DELETE:
                await asyncio.sleep(SELF_DELETE_SECONDS)
                await n.delete()         
    else:
        p = await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
        await asyncio.sleep(SELF_DELETE_SECONDS)
        await p.delete()
        if SELF_DELETE:
            await asyncio.sleep(SELF_DELETE_SECONDS)
            await p.delete()
    if spoll:
        await msg.message.delete()

# Born to make history @LazyDeveloper !
async def advantage_spell_chok(client, msg):
    mv_id = msg.id
    mv_rqst = msg.text
    reqstr1 = msg.from_user.id if msg.from_user else 0
    reqstr = await client.get_users(reqstr1)
    settings = await get_settings(msg.chat.id)
    query = re.sub(
        r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)",
        "", msg.text, flags=re.IGNORECASE)  # plis contribute some common words
    query = query.strip() + " movie"
    try:
        movies = await get_poster(mv_rqst, bulk=True)
    except Exception as e:
        logger.exception(e)
        reqst_gle = mv_rqst.replace(" ", "+")
        button = [[
        InlineKeyboardButton('🔍 sᴇᴀʀᴄʜ ᴏɴ ɢᴏᴏɢʟᴇ​ 🔎', url=f"https://www.google.com/search?q={reqst_gle}")            
        ]]
  
        k = await msg.reply_text(
            text=("sᴏʀʀʏ ɴᴏ ꜰɪʟᴇs ᴡᴇʀᴇ ꜰᴏᴜɴᴅ\n\nᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴘᴇʟʟɪɴɢ ɪɴ ɢᴏᴏɢʟᴇ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ !!"),
            reply_markup=InlineKeyboardMarkup(button),
            reply_to_message_id=msg.id
        )
        await asyncio.sleep(40)
        await k.delete()      
        return
    movielist = []
    if not movies:
        reqst_gle = mv_rqst.replace(" ", "+")
        button = [[
        InlineKeyboardButton('🔍 sᴇᴀʀᴄʜ ᴏɴ ɢᴏᴏɢʟᴇ​ 🔎', url=f"https://www.google.com/search?q={reqst_gle}")   
        ]]
        k = await msg.reply_text(
            text=("<b>sᴏʀʀʏ ɴᴏ ꜰɪʟᴇs ᴡᴇʀᴇ ꜰᴏᴜɴᴅ\n\nᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴘᴇʟʟɪɴɢ ɪɴ ɢᴏᴏɢʟᴇ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ !!</b>"),
            reply_markup=InlineKeyboardMarkup(button),
            reply_to_message_id=msg.id
        )
        await asyncio.sleep(40)
        await k.delete()
        return
    movielist = [movie.get('title') for movie in movies]
    SPELL_CHECK[mv_id] = movielist
    btn = [
        [
            InlineKeyboardButton(
                text=movie_name.strip(),
                callback_data=f"spol#{reqstr1}#{k}",
            )
        ]
        for k, movie_name in enumerate(movielist)
    ]
    btn.append([InlineKeyboardButton(text="Close", callback_data=f'spol#{reqstr1}#close_spellcheck')])
    #spell_check_del = await msg.reply_text(text=("<b><I>I Couldn't find anything related to that.\nDid you mean any of these?</I></b>"),reply_markup=InlineKeyboardMarkup(btn),reply_to_message_id=msg.id )

async def manual_filters(client, message, text=False):
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await client.send_message(group_id, reply_text, disable_web_page_preview=True)
                        else:
                            button = eval(btn)
                            await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                    elif btn == "[]":
                        await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                    else:
                        button = eval(btn)
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False

import telebot
from telebot import types
import json
import os
import html


# =========================================================
# CONFIG
# =========================================================

BOT_TOKEN = "8939223619:AAGj0DVcE-caFVNuige4NYfdmppnZyhDy8U"

bot = telebot.TeleBot(
    BOT_TOKEN,
    parse_mode="HTML"
)

DB_FILE = "database.json"

sessions = {}


# =========================================================
# MANDATORY JOIN CHANNELS
# =========================================================

JOIN_CHANNEL_1 = "@CHS_TEAM_OFFICIAL"
JOIN_CHANNEL_2 = "@ModderSanto_Official"

JOIN_CHANNEL_1_URL = "https://t.me/CHS_TEAM_OFFICIAL"
JOIN_CHANNEL_2_URL = "https://t.me/ModderSanto_Official"


# =========================================================
# HTML SAFE
# =========================================================

def safe_html(text):
    return html.escape(str(text))


# =========================================================
# DATABASE
# =========================================================

def load_db():

    if not os.path.exists(DB_FILE):

        return {
            "channels": {}
        }

    try:

        with open(
            DB_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

            if not isinstance(data, dict):
                data = {}

            if "channels" not in data:
                data["channels"] = {}

            return data

    except Exception:

        return {
            "channels": {}
        }


def save_db():

    with open(
        DB_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            db,
            f,
            indent=2,
            ensure_ascii=False
        )


db = load_db()


# =========================================================
# FORCE JOIN CHECK
# =========================================================

def check_joined(user_id):

    try:

        member1 = bot.get_chat_member(
            JOIN_CHANNEL_1,
            user_id
        )

        member2 = bot.get_chat_member(
            JOIN_CHANNEL_2,
            user_id
        )

        valid_status = [
            "member",
            "administrator",
            "creator"
        ]

        joined1 = member1.status in valid_status
        joined2 = member2.status in valid_status

        return joined1 and joined2

    except Exception:

        return False


# =========================================================
# JOIN KEYBOARD
# =========================================================

def join_keyboard():

    kb = types.InlineKeyboardMarkup(
        row_width=1
    )

    kb.add(
        types.InlineKeyboardButton(
            "🔵 Join Channel 1",
            url=JOIN_CHANNEL_1_URL
        )
    )

    kb.add(
        types.InlineKeyboardButton(
            "🟢 Join Channel 2",
            url=JOIN_CHANNEL_2_URL
        )
    )

    kb.add(
        types.InlineKeyboardButton(
            "✅ Verify Join",
            callback_data="verify_join"
        )
    )

    return kb


# =========================================================
# SEND JOIN MESSAGE
# =========================================================

def send_join_message(chat_id):

    bot.send_message(
        chat_id,
        """
<b>╭━━━━━━━━━━━━━━━━━━╮
       🔐 JOIN REQUIRED
╰━━━━━━━━━━━━━━━━━━╯</b>

🚀 Welcome to <b>PREMIUM POST MAKER</b>!

To use all bot features, you must
join both required channels.

━━━━━━━━━━━━━━━━━━

🔵 <b>Channel 1</b>

Join the first channel below.

🟢 <b>Channel 2</b>

Join the second channel below.

━━━━━━━━━━━━━━━━━━

After joining both channels,
press:

✅ <b>Verify Join</b>

⚠️ You cannot use the bot
until verification is completed.
""",
        reply_markup=join_keyboard()
    )


# =========================================================
# MAIN MENU
# =========================================================

def main_menu():

    kb = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2
    )

    kb.add(
        types.KeyboardButton(
            "🔵 📝 Create Post"
        ),
        types.KeyboardButton(
            "🟢 ➕ Add Channel"
        )
    )

    kb.add(
        types.KeyboardButton(
            "🟡 📢 My Channels"
        )
    )

    return kb


# =========================================================
# CANCEL KEYBOARD
# =========================================================

def cancel_keyboard():

    kb = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    kb.add(
        types.KeyboardButton(
            "🔴 Cancel"
        )
    )

    return kb


# =========================================================
# START
# =========================================================

@bot.message_handler(commands=["start"])
def start(message):

    user_id = message.from_user.id

    sessions.pop(
        user_id,
        None
    )

    # FORCE JOIN
    if not check_joined(user_id):

        send_join_message(
            message.chat.id
        )

        return

    text = """
<b>╭━━━━━━━━━━━━━━━━━━╮
   🚀 PREMIUM POST MAKER
╰━━━━━━━━━━━━━━━━━━╯</b>

✨ <b>Professional Channel Publisher</b>

🖼️ Photo
🎬 Video
📁 File
✍️ Caption
🔘 Multiple Buttons
📐 2 Buttons Per Row
📢 Multi Channel

━━━━━━━━━━━━━━━━━━

<b>Button Legend:</b>

🔵 Primary
🟢 Success
🟡 Warning
🔴 Danger

━━━━━━━━━━━━━━━━━━

👇 <b>Select an option:</b>
"""

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=main_menu()
    )


# =========================================================
# VERIFY JOIN
# =========================================================

@bot.callback_query_handler(
    func=lambda call:
        call.data == "verify_join"
)
def verify_join(call):

    user_id = call.from_user.id

    if check_joined(user_id):

        bot.answer_callback_query(
            call.id,
            "✅ Verification successful!"
        )

        try:

            bot.delete_message(
                call.message.chat.id,
                call.message.message_id
            )

        except Exception:

            pass

        bot.send_message(
            call.message.chat.id,
            """
<b>╭━━━━━━━━━━━━━━━━━━╮
       ✅ VERIFIED
╰━━━━━━━━━━━━━━━━━━╯</b>

🎉 Both channels joined successfully!

🚀 <b>PREMIUM POST MAKER</b>
is now unlocked.

👇 <b>Select an option:</b>
""",
            reply_markup=main_menu()
        )

    else:

        bot.answer_callback_query(
            call.id,
            "❌ Join both channels first!",
            show_alert=True
        )

        bot.send_message(
            call.message.chat.id,
            """
<b>╭━━━━━━━━━━━━━━━━━━╮
   ❌ VERIFICATION FAILED
╰━━━━━━━━━━━━━━━━━━╯</b>

You have not joined both required
channels yet.

━━━━━━━━━━━━━━━━━━

🔵 Join Channel 1
🟢 Join Channel 2

After joining both channels:

✅ <b>Verify Join</b>

━━━━━━━━━━━━━━━━━━

⚠️ Both channels are mandatory.
""",
            reply_markup=join_keyboard()
        )


# =========================================================
# CREATE POST
# =========================================================

@bot.message_handler(
    func=lambda message:
        message.text in [
            "🔵 📝 Create Post",
            "📝 Create Post"
        ]
)
def create_post_keyboard(message):

    if not check_joined(
        message.from_user.id
    ):

        send_join_message(
            message.chat.id
        )

        return

    sessions[
        message.from_user.id
    ] = {

        "step": "media",

        "media_type": None,

        "file_id": None,

        "caption": "",

        "buttons": []
    }

    bot.send_message(
        message.chat.id,
        """
<b>╭━━━━━━━━━━━━━━━━━━╮
       📝 CREATE POST
╰━━━━━━━━━━━━━━━━━━╯</b>

━━━━━━━━━━━━━━━━━━

Send your:

🖼️ <b>Photo</b>
🎬 <b>Video</b>
📁 <b>Document</b>

After that I'll ask for the
caption and buttons.

━━━━━━━━━━━━━━━━━━

🔴 <b>Cancel anytime:</b>

/cancel
""",
        reply_markup=cancel_keyboard()
    )


# =========================================================
# ADD CHANNEL
# =========================================================

@bot.message_handler(
    func=lambda message:
        message.text in [
            "🟢 ➕ Add Channel",
            "➕ Add Channel"
        ]
)
def add_channel_keyboard(message):

    if not check_joined(
        message.from_user.id
    ):

        send_join_message(
            message.chat.id
        )

        return

    bot_username = bot.get_me().username

    add_url = (
        f"https://t.me/{bot_username}"
        "?startchannel=botstart"
    )

    kb = types.InlineKeyboardMarkup(
        row_width=1
    )

    kb.add(
        types.InlineKeyboardButton(
            "🟢 Add Bot to Channel",
            url=add_url
        )
    )

    kb.add(
        types.InlineKeyboardButton(
            "🔵 Verify Channel",
            callback_data="verify_channel"
        )
    )

    kb.add(
        types.InlineKeyboardButton(
            "🔴 Close",
            callback_data="close_message"
        )
    )

    bot.send_message(
        message.chat.id,
        """
<b>╭━━━━━━━━━━━━━━━━━━╮
       ➕ ADD CHANNEL
╰━━━━━━━━━━━━━━━━━━╯</b>

<b>Step 1</b>

Add this bot to your Telegram Channel
as an <b>Administrator</b>.

<b>Step 2</b>

Give the bot permission to:

✅ Post Messages

<b>Step 3</b>

After adding the bot, press:

🔵 <b>Verify Channel</b>

━━━━━━━━━━━━━━━━━━

⚠️ Make sure the bot is already
an Administrator in your channel.
""",
        reply_markup=kb
    )


# =========================================================
# CLOSE INLINE MESSAGE
# =========================================================

@bot.callback_query_handler(
    func=lambda call:
        call.data == "close_message"
)
def close_message(call):

    bot.answer_callback_query(
        call.id,
        "Closed"
    )

    try:

        bot.delete_message(
            call.message.chat.id,
            call.message.message_id
        )

    except Exception:

        pass


# =========================================================
# VERIFY CHANNEL BUTTON
# =========================================================

@bot.callback_query_handler(
    func=lambda call:
        call.data == "verify_channel"
)
def verify_channel(call):

    if not check_joined(
        call.from_user.id
    ):

        bot.answer_callback_query(
            call.id,
            "❌ Join both required channels first!",
            show_alert=True
        )

        return

    bot.answer_callback_query(
        call.id
    )

    sessions[
        call.from_user.id
    ] = {
        "step": "channel_username"
    }

    bot.send_message(
        call.message.chat.id,
        """
<b>╭━━━━━━━━━━━━━━━━━━╮
       🔎 VERIFY CHANNEL
╰━━━━━━━━━━━━━━━━━━╯</b>

Send your channel username.

Example:

<code>@MyChannel</code>

━━━━━━━━━━━━━━━━━━

Make sure the bot is already an
<b>Administrator</b> in that channel.

🔴 /cancel
""",
        reply_markup=cancel_keyboard()
    )


# =========================================================
# RECEIVE CHANNEL
# =========================================================

@bot.message_handler(
    func=lambda message:
        message.from_user.id in sessions
        and
        sessions[
            message.from_user.id
        ].get("step") == "channel_username"
)
def receive_channel(message):

    user_id = message.from_user.id

    if not check_joined(user_id):

        send_join_message(
            message.chat.id
        )

        return

    if not message.text:

        bot.send_message(
            message.chat.id,
            "❌ Please send a channel username."
        )

        return

    channel = message.text.strip()

    if not channel.startswith("@"):

        bot.send_message(
            message.chat.id,
            """
❌ <b>INVALID CHANNEL USERNAME</b>

Please send it like:

<code>@MyChannel</code>
""",
            reply_markup=cancel_keyboard()
        )

        return

    try:

        chat = bot.get_chat(channel)

        me = bot.get_me()

        member = bot.get_chat_member(
            chat.id,
            me.id
        )

        if member.status not in [
            "administrator",
            "creator"
        ]:

            bot.send_message(
                message.chat.id,
                """
❌ <b>VERIFICATION FAILED</b>

The bot is not an administrator
in this channel.

Please add the bot as an
<b>Administrator</b> and try again.
""",
                reply_markup=cancel_keyboard()
            )

            return

        if member.status == "administrator":

            if hasattr(
                member,
                "can_post_messages"
            ):

                if member.can_post_messages is False:

                    bot.send_message(
                        message.chat.id,
                        """
❌ <b>POSTING PERMISSION MISSING</b>

Give the bot permission:

✅ Post Messages

Then try verification again.
""",
                        reply_markup=cancel_keyboard()
                    )

                    return

        db["channels"][
            str(chat.id)
        ] = {

            "title":
                chat.title or "Unknown Channel",

            "username":
                chat.username or channel,

            "owner":
                user_id
        }

        save_db()

        sessions.pop(
            user_id,
            None
        )

        channel_title = safe_html(
            chat.title or "Unknown Channel"
        )

        channel_username = safe_html(
            chat.username or channel
        )

        bot.send_message(
            message.chat.id,
            f"""
<b>╭━━━━━━━━━━━━━━━━━━╮
       🟢 CHANNEL ADDED
╰━━━━━━━━━━━━━━━━━━╯</b>

📢 <b>{channel_title}</b>

🔗 {channel_username}

🆔 <code>{chat.id}</code>

━━━━━━━━━━━━━━━━━━

✅ The bot can now publish posts
to this channel. 🚀
""",
            reply_markup=main_menu()
        )

    except Exception as e:

        error_text = safe_html(e)

        bot.send_message(
            message.chat.id,
            f"""
<b>❌ CHANNEL VERIFICATION ERROR</b>

<b>Possible reasons:</b>

• Username is incorrect
• Bot isn't admin
• Channel is inaccessible
• Bot has no posting permission

━━━━━━━━━━━━━━━━━━

<b>Error:</b>

<code>{error_text}</code>
""",
            reply_markup=cancel_keyboard()
        )


# =========================================================
# MY CHANNELS
# =========================================================

@bot.message_handler(
    func=lambda message:
        message.text in [
            "🟡 📢 My Channels",
            "📢 My Channels"
        ]
)
def my_channels_keyboard(message):

    if not check_joined(
        message.from_user.id
    ):

        send_join_message(
            message.chat.id
        )

        return

    channels = db.get(
        "channels",
        {}
    )

    if not channels:

        bot.send_message(
            message.chat.id,
            """
❌ <b>NO CHANNELS ADDED</b>

Please use:

🟢 <b>Add Channel</b>
""",
            reply_markup=main_menu()
        )

        return

    text = """
<b>╭━━━━━━━━━━━━━━━━━━╮
       📢 MY CHANNELS
╰━━━━━━━━━━━━━━━━━━╯</b>

"""

    for number, (
        channel_id,
        data
    ) in enumerate(
        channels.items(),
        1
    ):

        title = safe_html(
            data.get(
                "title",
                "Unknown Channel"
            )
        )

        username = safe_html(
            data.get(
                "username",
                "Unknown"
            )
        )

        text += (
            f"<b>{number}.</b> 📢 "
            f"{title}\n"
            f"   🔗 {username}\n"
            f"   🆔 <code>{safe_html(channel_id)}</code>\n\n"
        )

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=main_menu()
    )


# =========================================================
# MEDIA
# =========================================================

@bot.message_handler(
    content_types=[
        "photo",
        "video",
        "document"
    ]
)
def receive_media(message):

    user_id = message.from_user.id

    if not check_joined(user_id):

        send_join_message(
            message.chat.id
        )

        return

    if user_id not in sessions:
        return

    session = sessions[user_id]

    if session.get("step") != "media":
        return

    if message.photo:

        session["media_type"] = "photo"

        session["file_id"] = (
            message.photo[-1].file_id
        )

    elif message.video:

        session["media_type"] = "video"

        session["file_id"] = (
            message.video.file_id
        )

    elif message.document:

        session["media_type"] = "document"

        session["file_id"] = (
            message.document.file_id
        )

    session["step"] = "caption"

    bot.send_message(
        message.chat.id,
        """
<b>╭━━━━━━━━━━━━━━━━━━╮
       🟢 MEDIA RECEIVED
╰━━━━━━━━━━━━━━━━━━╯</b>

Now send the <b>Caption / Title</b>.

Example:

<code>🔥 Premium App Update

✨ Version 5.0
⚡ Fast & Smooth
📦 Download Now</code>

🔴 /cancel
""",
        reply_markup=cancel_keyboard()
    )


# =========================================================
# CAPTION
# =========================================================

@bot.message_handler(
    func=lambda message:
        message.from_user.id in sessions
        and
        sessions[
            message.from_user.id
        ].get("step") == "caption"
)
def receive_caption(message):

    user_id = message.from_user.id

    if not check_joined(user_id):

        send_join_message(
            message.chat.id
        )

        return

    if not message.text:

        bot.send_message(
            message.chat.id,
            "❌ Please send caption text."
        )

        return

    sessions[user_id]["caption"] = (
        message.text
    )

    sessions[user_id]["step"] = (
        "button_name"
    )

    bot.send_message(
        message.chat.id,
        """
<b>╭━━━━━━━━━━━━━━━━━━╮
       🔘 BUTTON BUILDER
╰━━━━━━━━━━━━━━━━━━╯</b>

Send your button name.

Example:

<code>📥 Download</code>

Or send:

<code>/skip</code>

to publish without buttons.

🔴 /cancel
""",
        reply_markup=cancel_keyboard()
    )


# =========================================================
# BUTTON NAME
# =========================================================

@bot.message_handler(
    func=lambda message:
        message.from_user.id in sessions
        and
        sessions[
            message.from_user.id
        ].get("step") == "button_name"
)
def button_name(message):

    user_id = message.from_user.id

    if not check_joined(user_id):

        send_join_message(
            message.chat.id
        )

        return

    if not message.text:
        return

    if message.text.strip().lower() == "/skip":

        sessions[user_id]["step"] = (
            "select_channel"
        )

        show_channels(
            message.chat.id
        )

        return

    sessions[user_id]["temp_name"] = (
        message.text.strip()
    )

    sessions[user_id]["step"] = (
        "button_link"
    )

    bot.send_message(
        message.chat.id,
        """
<b>╭━━━━━━━━━━━━━━━━━━╮
       🔗 BUTTON LINK
╰━━━━━━━━━━━━━━━━━━╯</b>

Send the button URL.

Example:

<code>https://example.com</code>

🔴 /cancel
""",
        reply_markup=cancel_keyboard()
    )


# =========================================================
# BUTTON LINK
# =========================================================

@bot.message_handler(
    func=lambda message:
        message.from_user.id in sessions
        and
        sessions[
            message.from_user.id
        ].get("step") == "button_link"
)
def button_link(message):

    user_id = message.from_user.id

    if not check_joined(user_id):

        send_join_message(
            message.chat.id
        )

        return

    if not message.text:

        bot.send_message(
            message.chat.id,
            "❌ Please send a valid URL."
        )

        return

    url = message.text.strip()

    if not (
        url.startswith("https://")
        or
        url.startswith("http://")
        or
        url.startswith("tg://")
    ):

        bot.send_message(
            message.chat.id,
            """
❌ <b>INVALID URL</b>

Please send a valid URL.

Example:

<code>https://example.com</code>
""",
            reply_markup=cancel_keyboard()
        )

        return

    button_name_text = (
        sessions[user_id]
        .get(
            "temp_name",
            "Button"
        )
    )

    sessions[user_id]["buttons"].append({

        "name":
            button_name_text,

        "url":
            url
    })

    sessions[user_id].pop(
        "temp_name",
        None
    )

    sessions[user_id].pop(
        "temp_url",
        None
    )

    sessions[user_id]["step"] = (
        "button_action"
    )

    total = len(
        sessions[user_id]["buttons"]
    )

    kb = types.InlineKeyboardMarkup(
        row_width=2
    )

    kb.add(
        types.InlineKeyboardButton(
            "🟢 Add Button",
            callback_data="add_more_button"
        ),

        types.InlineKeyboardButton(
            "🔵 Publish",
            callback_data="publish_post"
        )
    )

    kb.add(
        types.InlineKeyboardButton(
            "🔴 Cancel",
            callback_data="cancel_post"
        )
    )

    safe_name = safe_html(
        button_name_text
    )

    bot.send_message(
        message.chat.id,
        f"""
<b>╭━━━━━━━━━━━━━━━━━━╮
       🟢 BUTTON ADDED
╰━━━━━━━━━━━━━━━━━━╯</b>

🔘 <b>{safe_name}</b>

🔢 Total Buttons:
<b>{total}</b>

━━━━━━━━━━━━━━━━━━

🟢 Add more buttons
🔵 Publish the post
🔴 Cancel
""",
        reply_markup=kb
    )


# =========================================================
# ADD MORE BUTTON
# =========================================================

@bot.callback_query_handler(
    func=lambda call:
        call.data == "add_more_button"
)
def add_more_button(call):

    user_id = call.from_user.id

    if not check_joined(user_id):

        bot.answer_callback_query(
            call.id,
            "❌ Join both channels first!",
            show_alert=True
        )

        return

    if user_id not in sessions:

        bot.answer_callback_query(
            call.id,
            "Session expired."
        )

        return

    sessions[user_id]["step"] = (
        "button_name"
    )

    bot.answer_callback_query(
        call.id,
        "Add next button"
    )

    bot.send_message(
        call.message.chat.id,
        """
<b>╭━━━━━━━━━━━━━━━━━━╮
       🟢 ADD BUTTON
╰━━━━━━━━━━━━━━━━━━╯</b>

Send the next button name.

Example:

<code>📥 Download</code>

🔴 /cancel
""",
        reply_markup=cancel_keyboard()
    )


# =========================================================
# PUBLISH BUTTON
# =========================================================

@bot.callback_query_handler(
    func=lambda call:
        call.data == "publish_post"
)
def publish_button(call):

    user_id = call.from_user.id

    if not check_joined(user_id):

        bot.answer_callback_query(
            call.id,
            "❌ Join both channels first!",
            show_alert=True
        )

        return

    if user_id not in sessions:

        bot.answer_callback_query(
            call.id,
            "Session expired."
        )

        return

    sessions[user_id]["step"] = (
        "select_channel"
    )

    bot.answer_callback_query(
        call.id,
        "Select channel"
    )

    show_channels(
        call.message.chat.id
    )


# =========================================================
# CANCEL POST
# =========================================================

@bot.callback_query_handler(
    func=lambda call:
        call.data == "cancel_post"
)
def cancel_post(call):

    user_id = call.from_user.id

    sessions.pop(
        user_id,
        None
    )

    bot.answer_callback_query(
        call.id,
        "Cancelled"
    )

    bot.send_message(
        call.message.chat.id,
        """
🔴 <b>POST CANCELLED</b>

You are back to the Main Menu. 🏠
""",
        reply_markup=main_menu()
    )


# =========================================================
# SHOW CHANNELS
# =========================================================

def show_channels(chat_id):

    channels = db.get(
        "channels",
        {}
    )

    if not channels:

        bot.send_message(
            chat_id,
            """
❌ <b>NO CHANNEL FOUND</b>

Please add a channel first.

🟢 Add Channel
""",
            reply_markup=main_menu()
        )

        return

    kb = types.InlineKeyboardMarkup(
        row_width=1
    )

    for channel_id, data in channels.items():

        title = safe_html(
            data.get(
                "title",
                "Unknown Channel"
            )
        )

        kb.add(
            types.InlineKeyboardButton(
                f"🔵 📢 {title}",
                callback_data=(
                    f"publish_to:{channel_id}"
                )
            )
        )

    kb.add(
        types.InlineKeyboardButton(
            "🔴 Cancel",
            callback_data="cancel_post"
        )
    )

    bot.send_message(
        chat_id,
        """
<b>╭━━━━━━━━━━━━━━━━━━╮
       📢 SELECT CHANNEL
╰━━━━━━━━━━━━━━━━━━╯</b>

Choose the channel where the post
should be published.

🔵 Select Channel
🔴 Cancel
""",
        reply_markup=kb
    )


# =========================================================
# PUBLISH TO CHANNEL
# =========================================================

@bot.callback_query_handler(
    func=lambda call:
        call.data.startswith("publish_to:")
)
def publish_to_channel(call):

    user_id = call.from_user.id

    if not check_joined(user_id):

        bot.answer_callback_query(
            call.id,
            "❌ Join both channels first!",
            show_alert=True
        )

        return

    if user_id not in sessions:

        bot.answer_callback_query(
            call.id,
            "Session expired."
        )

        return

    channel_id = call.data.split(
        ":",
        1
    )[1]

    if channel_id not in db.get(
        "channels",
        {}
    ):

        bot.answer_callback_query(
            call.id,
            "Channel not found."
        )

        return

    session = sessions[user_id]

    media_type = session.get(
        "media_type"
    )

    file_id = session.get(
        "file_id"
    )

    # IMPORTANT:
    # Escape caption so user-entered < > & do not
    # break Telegram HTML parser.
    caption = safe_html(
        session.get(
            "caption",
            ""
        )
    )

    buttons = session.get(
        "buttons",
        []
    )

    keyboard = None

    if buttons:

        keyboard = types.InlineKeyboardMarkup(
            row_width=2
        )

        row = []

        for button in buttons:

            name = safe_html(
                button.get(
                    "name",
                    "Button"
                )
            )

            url = button.get(
                "url",
                ""
            )

            row.append(
                types.InlineKeyboardButton(
                    text=name,
                    url=url
                )
            )

            if len(row) == 2:

                keyboard.row(
                    *row
                )

                row = []

        if row:

            keyboard.row(
                *row
            )

    try:

        if media_type == "photo":

            bot.send_photo(
                chat_id=channel_id,
                photo=file_id,
                caption=caption,
                reply_markup=keyboard
            )

        elif media_type == "video":

            bot.send_video(
                chat_id=channel_id,
                video=file_id,
                caption=caption,
                reply_markup=keyboard
            )

        elif media_type == "document":

            bot.send_document(
                chat_id=channel_id,
                document=file_id,
                caption=caption,
                reply_markup=keyboard
            )

        else:

            raise Exception(
                "Invalid media type."
            )

        channel_name = safe_html(
            db[
                "channels"
            ][channel_id].get(
                "title",
                "Unknown Channel"
            )
        )

        sessions.pop(
            user_id,
            None
        )

        bot.answer_callback_query(
            call.id,
            "Post published!"
        )

        bot.send_message(
            call.message.chat.id,
            f"""
<b>╭━━━━━━━━━━━━━━━━━━╮
       🎉 PUBLISHED
╰━━━━━━━━━━━━━━━━━━╯</b>

📢 Channel:
<b>{channel_name}</b>

🔘 Buttons:
<b>{len(buttons)}</b>

━━━━━━━━━━━━━━━━━━

🟢 <b>Post successfully published.</b>
""",
            reply_markup=main_menu()
        )

    except Exception as e:

        error_text = safe_html(e)

        bot.answer_callback_query(
            call.id,
            "Publish failed!"
        )

        bot.send_message(
            call.message.chat.id,
            f"""
<b>❌ PUBLISH ERROR</b>

Something went wrong while
publishing the post.

━━━━━━━━━━━━━━━━━━

<b>Error:</b>

<code>{error_text}</code>
""",
            reply_markup=main_menu()
        )


# =========================================================
# CANCEL COMMAND
# =========================================================

@bot.message_handler(
    commands=["cancel"]
)
def cancel(message):

    sessions.pop(
        message.from_user.id,
        None
    )

    bot.send_message(
        message.chat.id,
        """
🔴 <b>OPERATION CANCELLED</b>

You are back to the Main Menu. 🏠
""",
        reply_markup=main_menu()
    )


# =========================================================
# CANCEL REPLY BUTTON
# =========================================================

@bot.message_handler(
    func=lambda message:
        message.text == "🔴 Cancel"
)
def cancel_button(message):

    sessions.pop(
        message.from_user.id,
        None
    )

    bot.send_message(
        message.chat.id,
        """
🔴 <b>OPERATION CANCELLED</b>

You are back to the Main Menu. 🏠
""",
        reply_markup=main_menu()
    )


# =========================================================
# UNKNOWN TEXT
# =========================================================

@bot.message_handler(
    func=lambda message:
        True
)
def unknown_message(message):

    user_id = message.from_user.id

    if not check_joined(user_id):

        send_join_message(
            message.chat.id
        )

        return

    if user_id in sessions:
        return

    bot.send_message(
        message.chat.id,
        """
❓ <b>UNKNOWN COMMAND</b>

Please use the buttons below.

👇 <b>Main Menu</b>
""",
        reply_markup=main_menu()
    )


# =========================================================
# RUN BOT
# =========================================================

print(
    "🚀 PREMIUM POST MAKER STARTED"
)

bot.infinity_polling(
    skip_pending=True
)
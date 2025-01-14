from pyrogram import Client, enums

cyber_ = """
Copyright (C) 2025-2026 by TheHamkerGuy@Github, < https://github.com/TheHamkerGuy/CyberUserbot >.
This file is part of < https://github.com/TheHamkerGuy/CyberUserbot > project,
and is released under the "GNU v3.0 License Agreement".
Please see < https://github.com/TheHamkerGuy/CyberUserbot/blob/main/LICENSE >
All rights reserved.
"""

print(cyber_)

api_id = input("Enter Your API ID: \n")
api_hash = input("Enter Your API HASH : \n")

with Client("my_account", api_id=api_id, api_hash=api_hash, hide_password=True) as bot_:
    first_name = (bot_.get_me()).first_name
    string_session_ = f"<b><u>String Session For {first_name}</b></u> \n<code>{bot_.export_session_string()}</code>"
    bot_.send_message("me", string_session_, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
    print(f"String Has Been Sent To Your Saved Message : {first_name}")

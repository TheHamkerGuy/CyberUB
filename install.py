from datetime import datetime
import sys
from pyrogram import Client

from utils import config

common_params = {
    "api_id": config.api_id,
    "api_hash": config.api_hash,
    "hide_password": True,
    "test_mode": config.test_server,
}

if __name__ == "__main__":
    if config.STRINGSESSION:
        common_params["session_string"] = config.STRINGSESSION

    app = Client("my_account", **common_params)

    if config.db_type in ["mongo", "mongodb"]:
        from pymongo import MongoClient, errors

        db = MongoClient(config.db_url)
        try:
            db.server_info()
        except errors.ConnectionFailure as e:
            raise RuntimeError(
                "MongoDB server isn't available! "
                f"Provided url: {config.db_url}. "
                "Enter valid URL and restart installation"
            ) from e

    install_type = sys.argv[1] if len(sys.argv) > 1 else "3"
    if install_type == "1":
        restart = "pm2 restart Moon"
    elif install_type == "2":
        restart = "sudo systemctl restart Moon"
    else:
        restart = "cd CyberUserbot/ && python main.py"

    app.start()
    try:
        app.send_message(
            "me",
            f"<b>[{datetime.now()}] CyberUserbot launched! \n"
            "Channel: @Cyber_Userbot_News\n"
            "Chat: @Cyber_Userbot_Support\n"
            f"For restart, enter:</b>\n"
            f"<code>{restart}</code>",
        )
    except Exception as e:
        print(f"[ERROR]: Sending Message to me failed! {e}")
    app.stop()

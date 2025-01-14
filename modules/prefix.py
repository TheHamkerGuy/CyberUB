from pyrogram import Client, filters
from pyrogram.types import Message

from utils.db import db
from utils.misc import modules_help, prefix
from utils.scripts import restart


@Client.on_message(
    filters.command(["sp", "setprefix", "setprefix_Moon"], prefix) & filters.me
)
async def setprefix(_, message: Message):
    if len(message.command) > 1:
        pref = message.command[1]
        db.set("core.main", "prefix", pref)
        await message.edit(
            f"<b>Prefix [ <code>{pref}</code> ] is set!\nRestarting...</b>"
        )
        db.set(
            "core.updater",
            "restart_info",
            {
                "type": "restart",
                "chat_id": message.chat.id,
                "message_id": message.id,
            },
        )
        restart()
    else:
        await message.edit("<b>The prefix must not be empty!</b>")


modules_help["prefix"] = {
    "setprefix [prefix]": "Set custom prefix",
    "setprefix_Moon [prefix]": "Set custom prefix",
}

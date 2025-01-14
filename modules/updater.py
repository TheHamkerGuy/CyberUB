import os
import sys
import shutil
import subprocess

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix, requirements_list
from utils.db import db
from utils.scripts import format_exc, restart


def check_command(command):
    return shutil.which(command) is not None


@Client.on_message(filters.command("restart", prefix) & filters.me)
async def restart_cmd(_, message: Message):
    db.set(
        "core.updater",
        "restart_info",
        {
            "type": "restart",
            "chat_id": message.chat.id,
            "message_id": message.id,
        },
    )

    if "LAVHOST" in os.environ:
        await message.edit("<b>Your lavHost is restarting...</b>")
        os.system("lavhost restart")
        return

    await message.edit("<b>Restarting...</b>")
    if os.path.exists("moonlogs.txt"):
        os.remove("moonlogs.txt")
    restart()


@Client.on_message(filters.command("update", prefix) & filters.me)
async def update(_, message: Message):
    db.set(
        "core.updater",
        "restart_info",
        {
            "type": "update",
            "chat_id": message.chat.id,
            "message_id": message.id,
        },
    )

    if "LAVHOST" in os.environ:
        await message.edit("<b>Your lavHost is updating...</b>")
        os.system("lavhost update")
        return

    await message.edit("<b>Updating...</b>")
    try:
        if not check_command("termux-setup-storage"):
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-U", "pip"], check=True
            )
        subprocess.run(["git", "pull"], check=True)
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-U",
                "-r",
                "requirements.txt",
            ],
            check=True,
        )
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-U", *requirements_list],
            check=True,
        )
    except Exception as e:
        await message.edit(format_exc(e))
        db.remove("core.updater", "restart_info")
    else:
        await message.edit("<b>Updating: done! Restarting...</b>")
        if os.path.exists("moonlogs.txt"):
            os.remove("moonlogs.txt")
        restart()


modules_help["updater"] = {
    "update": "Update the userbot. If new core modules are avaliable, they will be installed",
    "restart": "Restart userbot",
}

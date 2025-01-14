from pyrogram import Client, filters
from pyrogram.types import Message
import random
import datetime

from utils.misc import modules_help, prefix, userbot_version, python_version, gitrepo


@Client.on_message(filters.command(["support", "repo"], prefix) & filters.me)
async def support(_, message: Message):
    devs = ["@KRISHSUP3RYO"]
    random.shuffle(devs)

    commands_count = 0.0
    for module in modules_help:
        for _cmd in module:
            commands_count += 1

    await message.edit(
        f"<b>CyberUserbot\n\n"
        "GitHub: <a href=https://github.com/CyberUB/CyberUserbot>CyberUserbot</a>\n"
        "License: <a href=https://github.com/CyberUB/CyberUserbot/blob/master/LICENSE>GNU GPL v3</a>\n\n"
        "Channel: @Cyber_Userbot_News\n"
        "Chat [EN]: @Cyber_Userbot_Support\n"
        f"Main developers: {', '.join(devs)}\n\n"
        f"Python version: {python_version}\n"
        f"Modules count: {len(modules_help) / 1}\n"
        f"Commands count: {commands_count}</b>",
        disable_web_page_preview=True,
    )


@Client.on_message(filters.command(["version", "ver"], prefix) & filters.me)
async def version(client: Client, message: Message):
    changelog = ""
    ub_version = ".".join(userbot_version.split(".")[:2])
    async for m in client.search_messages("cyberuserbot", query=f"{userbot_version}."):
        if ub_version in m.text:
            changelog = m.message_id

    await message.delete()

    remote_url = list(gitrepo.remote().urls)[0]
    commit_time = (
        datetime.datetime.fromtimestamp(gitrepo.head.commit.committed_date)
        .astimezone(datetime.timezone.utc)
        .strftime("%Y-%m-%d %H:%M:%S %Z")
    )

    await message.reply(
        f"<b>Cyber Userbot version: {userbot_version}\n"
        f"Changelog </b><i><a href=https://t.me/Cyber_Userbot_News/{changelog}>in channel</a></i>.<b>\n"
        f"Changelog written by </b><i>"
        f"<a href=https://t.me/TheHamkerGuy>TheHamkerGuy</a></i>\n\n"
        + (
            f"<b>Branch: <a href={remote_url}/tree/{gitrepo.active_branch}>{gitrepo.active_branch}</a>\n"
            if gitrepo.active_branch != "master"
            else ""
        )
        + f"Commit: <a href={remote_url}/commit/{gitrepo.head.commit.hexsha}>"
        f"{gitrepo.head.commit.hexsha[:7]}</a> by {gitrepo.head.commit.author.name}\n"
        f"Commit time: {commit_time}</b>",
    )


modules_help["support"] = {
    "support": "Information about userbot",
    "version": "Check userbot version",
}

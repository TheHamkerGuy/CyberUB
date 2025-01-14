import datetime
import os
import time

import aiofiles
from pyrogram import Client, filters
from pyrogram.errors import MessageTooLong
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import edit_or_reply, format_exc, progress
from utils.rentry import new


async def read_file(file_path):
    async with aiofiles.open(file_path, mode="r") as file:
        content = await file.read()
    return content


def check_extension(file_path):
    extensions = {
        ".txt": "<pre lang='plaintext'>",
        ".py": "<pre lang='python'>",
        ".js": "<pre lang='javascript'>",
        ".json": "<pre lang='json'>",
        ".smali": "<pre lang='smali'>",
        ".sh": "<pre lang='shell'>",
        ".c": "<pre lang='c'>",
        ".java": "<pre lang='java'>",
        ".php": "<pre lang='php'>",
        ".doc": "<pre lang='doc'>",
        ".docx": "<pre lang='docx'>",
        ".rtf": "<pre lang='rtf'>",
        ".s": "<pre lang='asm'>",
        ".dart": "<pre lang='dart'>",
        ".cfg": "<pre lang='cfg'>",
        ".swift": "<pre lang='swift'>",
        ".cs": "<pre lang='csharp'>",
        ".vb": "<pre lang='vb'>",
        ".css": "<pre lang='css'>",
        ".htm": "<pre lang='html'>",
        ".html": "<pre lang='html'>",
        ".rss": "<pre lang='xml'>",
        ".xhtml": "<pre lang='xtml'>",
        ".cpp": "<pre lang='cpp'>",
    }

    ext = os.path.splitext(file_path)[1].lower()

    return extensions.get(ext, "<pre>")


@Client.on_message(filters.command("open", prefix) & filters.me)
async def openfile(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.edit_text("Kindly Reply to a File")

    try:
        ms = await edit_or_reply(message, "<b>Downloading...</b>")
        ct = time.time()
        file_path = await message.reply_to_message.download(
            progress=progress, progress_args=(ms, ct, "Downloading...")
        )
        await ms.edit_text("<code>Trying to open file...</code>")
        file_info = os.stat(file_path)
        file_name = file_path.split("/")[-1:]
        file_size = file_info.st_size
        last_modified = datetime.datetime.fromtimestamp(file_info.st_mtime).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        code_start = check_extension(file_path=file_path)
        content = await read_file(file_path=file_path)
        await ms.edit_text(
            f"<b>File Name:</b> <code>{file_name[0]}</code>\n<b>Size:</b> <code>{file_size} bytes</code>\n<b>Last Modified:</b> <code>{last_modified}</code>\n<b>Content:</b> {code_start}{content}</pre>",
        )

    except MessageTooLong:
        await ms.edit_text(
            "<code>File Content is too long... Pasting to rentry...</code>"
        )
        content_new = f"```{code_start[11:-2]}\n{content}```"
        paste = new(url="", edit_code="", text=content_new)
        if paste["status"] != "200":
            await ms.edit_text(f"<b>Error:</b> <code>{paste['content']}</code>")
            return
        await client.send_message(
            "me",
            f"Here's your edit code for Url: {paste['url']}\nEdit code:  <code>{paste['edit_code']}</code>",
            disable_web_page_preview=True,
        )
        await ms.edit_text(
            f"<b>File Name:</b> <code>{file_name[0]}</code>\n<b>Size:</b> <code>{file_size} bytes</code>\n<b>Last Modified:</b> <code>{last_modified}</code>\n<b>Content:</b> {paste['url']}\n<b>Note:</b> <code>Edit Code has been sent to your saved messages</code>",
            disable_web_page_preview=True,
        )

    except Exception as e:
        await ms.edit_text(format_exc(e))

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


modules_help["open"] = {
    "open": "Open content of any text supported filetype and show it's raw data"
}

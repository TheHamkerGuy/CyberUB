from contextlib import redirect_stdout
from io import StringIO

from pyrogram import Client, filters
from pyrogram.types import Message

# noinspection PyUnresolvedReferences
from utils.misc import modules_help, prefix
from utils.scripts import format_exc

# noinspection PyUnresolvedReferences


# noinspection PyUnusedLocal
@Client.on_message(
    filters.command(["ex", "exec", "py", "exnoedit"], prefix) & filters.me
)
async def user_exec(client: Client, message: Message):
    if len(message.command) == 1:
        await message.edit("<b>Code to execute isn't provided</b>")
        return

    code = message.text.split(maxsplit=1)[1]
    stdout = StringIO()

    await message.edit("<b>Executing...</b>")

    try:
        with redirect_stdout(stdout):
            exec(code)
        text = (
            "<b>Code:</b>\n"
            f"<code>{code}</code>\n\n"
            "<b>Result</b>:\n"
            f"<code>{stdout.getvalue()}</code>"
        )
        if message.command[0] == "exnoedit":
            await message.reply(text)
        else:
            await message.edit(text)
    except Exception as e:
        await message.edit(format_exc(e))


# noinspection PyUnusedLocal
@Client.on_message(filters.command(["ev", "eval"], prefix) & filters.me)
async def user_eval(client: Client, message: Message):
    if len(message.command) == 1:
        await message.edit("<b>Code to eval isn't provided</b>")
        return

    code = message.text.split(maxsplit=1)[1]

    try:
        result = eval(code)
        await message.edit(
            "<b>Expression:</b>\n"
            f"<code>{code}</code>\n\n"
            "<b>Result</b>:\n"
            f"<code>{result}</code>"
        )
    except Exception as e:
        await message.edit(format_exc(e))


modules_help["python"] = {
    "ex [python code]": "Execute Python code",
    "exnoedit [python code]": "Execute Python code and return result with reply",
    "eval [python code]": "Eval Python code",
}

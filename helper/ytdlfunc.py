from __future__ import unicode_literals
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import youtube_dl
from utils.util import humanbytes
import asyncio


def buttonmap(item):
    quality = item['format']
    if "audio" in quality.lower():
        return [InlineKeyboardButton(
            f"{quality} 🎵 {humanbytes(item['filesize'])}",
            callback_data=f"ytdata||audio||{item['format_id']}||{item['yturl']}"
        )]
    else:
        return [InlineKeyboardButton(
            f"{quality} 📹 {humanbytes(item['filesize'])}",
            callback_data=f"ytdata||video||{item['format_id']}||{item['yturl']}"
        )]


# Return a list of buttons
def create_buttons(qualitylist):
    return list(map(buttonmap, qualitylist))


# Extract YouTube info
def extractYt(yturl):
    ydl = youtube_dl.YoutubeDL()
    with ydl:
        qualityList = []
        r = ydl.extract_info(yturl, download=False)
        for fmt in r['formats']:
            # Filter dash video (without audio)
            if "dash" not in str(fmt['format']).lower():
                qualityList.append({
                    "format": fmt['format'],
                    "filesize": fmt['filesize'],
                    "format_id": fmt['format_id'],
                    "yturl": yturl
                })

        return r['title'], r['thumbnail'], qualityList


# Async download video using CLI
async def downloadvideocli(command_to_exec):
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    print("Download error:", e_response)
    filename = t_response.split("Merging formats into")[-1].split('"')[1]
    return filename


# Async download audio using CLI
async def downloadaudiocli(command_to_exec):
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    print("Download error:", e_response)

    return t_response.split("Destination")[-1].split("Deleting")[0].split(":")[-1].strip()

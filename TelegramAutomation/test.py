from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from tqdm import tqdm
import os
import datetime
api_id = "27881570"
api_hash = 'c20f398daa6da6600977ce6abab3bfb0'
phone_number = '+91-8303013790'
session_name = 'new_session_name'

def download_messages(channel, client, name):
    three_days_ago = datetime.datetime.now() - datetime.timedelta(days=3)
    messages = client.get_messages(channel, limit=2000, offset_date=three_days_ago)
    output_dir = f'./{name}/messages/'
    os.makedirs(output_dir, exist_ok=True)
    for message in tqdm(messages, desc="Downloading messages"):
        if message.text is not None:
            with open(f'{output_dir}{message.id}.txt', 'w', encoding='utf-8') as file:
                file.write(message.text)

def download_media(channel, client, name):
    three_days_ago = datetime.datetime.now() - datetime.timedelta(days=3)
    messages = client.get_messages(channel, limit=2000, offset_date=three_days_ago)
    output_dir = f'./{name}/media/'
    os.makedirs(output_dir, exist_ok=True)
    for message in tqdm(messages, desc="Downloading media"):
        if message.media:
            message.download_media(output_dir)

def download_files(channel, client, name):
    three_days_ago = datetime.datetime.now() - datetime.timedelta(days=3)
    messages = client.get_messages(channel, limit=2000, offset_date=three_days_ago)
    output_dir = f'./{name}/files/'
    os.makedirs(output_dir, exist_ok=True)
    for message in tqdm(messages, desc="Downloading files"):
        if message.file:
            message.download_media(output_dir)

def main():
    with TelegramClient(session_name, api_id, api_hash) as client:
        result = client(GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=500,
            hash=0,
        ))
        title = 'Stock Trading Jackpot®' 
        for chat in result.chats:
            # print(chat.title)
            if chat.title == title:
                download_messages(chat, client, "data")
                # download_media(chat, client, "data")
                # download_files(chat, client, "data")
                break

if __name__ == '__main__':
    main()
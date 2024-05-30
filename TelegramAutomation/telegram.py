from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import InputPeerEmpty
from tqdm import tqdm
import os
import datetime
import spacy
import json

# Replace the values with your own API ID, API hash, and phone number
api_id = "27881570"
api_hash = 'c20f398daa6da6600977ce6abab3bfb0'
phone_number = '+91-8303013790'
group_name = -1001367269053  # Replace with your group/channel ID
session_name = 'session_name'


nlp = spacy.load('en_core_web_sm')

def download_messages(channel, client, name):
    ten_days_ago = datetime.datetime.now() - datetime.timedelta(days=10)
    messages = client.get_messages(channel, limit=10000, offset_date=ten_days_ago)
    output_dir = f'./{name}/messages/'
    os.makedirs(output_dir, exist_ok=True)
    
   
    trade_calls_by_date = {}
    
    for message in tqdm(messages, desc="Downloading messages"):
        if message.text is not None:
            with open(f'{output_dir}{message.id}.txt', 'w', encoding='utf-8') as file:
                file.write(message.text)
                
         
            doc = nlp(message.text)
            
            
            for ent in doc.ents:
                if ent.label_ == 'ORG':
                   
                    if is_financial_org(ent.text) and is_trade_call(message.text):
                      
                        message_date = message.date.strftime('%Y-%m-%d')
                        
                    
                        if message_date in trade_calls_by_date:
                            trade_calls_by_date[message_date].append(message.text)
                        else:
                            trade_calls_by_date[message_date] = [message.text]
                        break
    
    # Save trade_calls_by_date as JSON
    with open(f'{output_dir}trade_calls_by_date.json', 'w') as json_file:
        json.dump(trade_calls_by_date, json_file, indent=4)
    
    print("Trade Calls by Date:")
    print(trade_calls_by_date)

def is_financial_org(text):
    financial_keywords = ['stock', 'trade', 'market', 'invest', 'finance', 'broker']
    financial_phrases = ['stock market', 'financial advisor', 'investment firm', 'trading platform']
    
    for keyword in financial_keywords:
        if keyword in text.lower():
            return True
    
    for phrase in financial_phrases:
        if phrase in text.lower():
            return True
    
    return False

def is_trade_call(text):
    trade_keywords = ['buy', 'sell', 'long', 'short', 'entry', 'exit', 'recommendation', 'target']
    trade_phrases = ['buy recommendation', 'sell recommendation', 'long position', 'short position', 'entry point', 'exit point']
    
    for keyword in trade_keywords:
        if keyword in text.lower():
            return True
    
    for phrase in trade_phrases:
        if phrase in text.lower():
            return True
    
    return False


def download_media(channel, client, name):
    messages = client.get_messages(channel, limit=2000)
    output_dir = f'./{name}/media/'
    os.makedirs(output_dir, exist_ok=True)
    
    for message in tqdm(messages, desc="Downloading media"):
        if message.media:
            message.download_media(output_dir)

def download_files(channel, client, name):
    messages = client.get_messages(channel, limit=2000)
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

        # title = 'Stock Trading Jackpot®' 
        title = 'Trade Phoenix' 
        for chat in result.chats:
            if chat.title == title:
                download_messages(chat, client, title)
                # download_media(chat, client, title)
                # download_files(chat, client, title)
                break

if __name__ == '__main__':
    main()

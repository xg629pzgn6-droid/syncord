import discord
from core.setup import get_bot_token, get_guild_id
import asyncio
from core.setup import BASE_DIR
from pathlib import Path

async def _upload_files(files:list[Path])->list[int]:
    """
    only purpose is to upload files to discord and return the message ids.
    """
    message_ids = []
    try:
        guild_id = get_guild_id()
        bot_token = get_bot_token()
        intents = discord.Intents.default()
        client = discord.Client(intents=intents)
        
        @client.event
        async def on_ready():
            guild = discord.utils.get(client.guilds, id=guild_id)
            channel = [x for x in guild.text_channels if x.name == "syncord"]
            print("Available Channels: ", "".join([x.name for x in channel]))
            if len(channel) == 0:
                print("Syncord Channel doesn't exist, Creating syncord channel...")
                channel = await guild.create_text_channel("syncord")
            else:
                print("Syncord Channel found.")
                channel = channel[0]
            for file_path in files:
                print(f"Uploading file: {file_path} to Discord...")
                discord_file = discord.File(fp=file_path, filename=str(file_path).split("\\")[-1])
                message = await channel.send(file=discord_file)
                print(f"Uploaded file: {file_path} as message ID: {message.id}")
                message_ids.append(message.id)
            
            print("All files uploaded, closing client...")
            await client.close()
            
        await client.start(bot_token)
    except Exception as e:
        pass
    return message_ids
    
    
    
async def _bulk_download_file(message_ids:list[int], uuid:str):
    """
    downloads a file from discord based on message id
    """
    files = []
    try:
        guild_id = get_guild_id()
        bot_token = get_bot_token()
        intents = discord.Intents.default()
        client = discord.Client(intents=intents)
        
        @client.event
        async def on_ready():
            guild = discord.utils.get(client.guilds, id=guild_id)
            channel = [x for x in guild.text_channels if x.name == "syncord"]
            if len(channel) == 0:
                raise Exception("Syncord channel not found!")
            else:
                channel = channel[0]
            
            for message_id in message_ids:
                message = await channel.fetch_message(message_id)
                for attachment in message.attachments:
                    await attachment.save(fp= BASE_DIR/'files'/uuid/attachment.filename)
                    files.append(BASE_DIR/'files'/uuid/attachment.filename)
            
            await client.close()
            
        await client.start(bot_token)
    except Exception as e:
        pass
    return files
    
def upload_files(files:list[Path])->list[int]:
    """
    - uploads the files to discord
    - returns the message ids list
    """
    return asyncio.run(_upload_files(files))

def bulk_download_files(message_ids:list[int], uuid:str)->list[Path]:
    """
    - downloads the files from discord based on message ids
    """
    return asyncio.run(_bulk_download_file(message_ids, uuid))
    
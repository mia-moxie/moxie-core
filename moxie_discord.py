import discord
import os
import moxie_chat_integration

BOT_TOKEN = os.environ.get('MOXIE_DISCORD_TOKEN')
HOME_CHANNEL = "ai-derping"

intents = discord.Intents.all()
intents.messages = True

bot = discord.Client(intents=intents)

chat = moxie_chat_integration.MoxieChat()

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.channel.name == HOME_CHANNEL:
        reply = await chat.receive_message(message.author, message.content)
        await send_message(reply)

async def send_message(message):
    if message is None or message.strip() == "":
        return

    channel = discord.utils.get(bot.get_all_channels(), name=HOME_CHANNEL)
    message_parts = [message[i:i + 1500] for i in range(0, len(message), 1500)]

    for part in message_parts:
        await channel.send(part)

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
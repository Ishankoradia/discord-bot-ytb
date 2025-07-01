import discord
from discord.ext import commands
from discord.message import Message
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """Event triggered when the bot is ready"""
    print(f"🤖 Bot is ready! Logged in as {bot.user.name} (ID: {bot.user.id})")
    print(f"📊 Connected to {len(bot.guilds)} servers")
    print("---" * 20)


@bot.event
async def on_message(message: Message):
    """Event triggered when a message is sent in channels or threads"""
    # Don't respond to bot messages
    if message.author.bot:
        return

    # Only process messages from text channels, threads, forum channels, and announcement channels
    if isinstance(
        message.channel,
        (
            discord.TextChannel,
            discord.Thread,
            discord.ForumChannel,
        ),
    ):
        print(f"📝 Message: {message.content}")
        print(f"👤 Author: {message.author.name} (ID: {message.author.id})")
        print(f"🏠 Guild: {message.guild.name}")

        if isinstance(message.channel, discord.Thread):
            print(f"🧵 Thread: {message.channel.name}")
            if hasattr(message.channel.parent, "name"):
                print(f"📍 Parent Channel: {message.channel.parent.name}")
        elif isinstance(message.channel, discord.ForumChannel):
            print(f"🗂️ Forum Channel: {message.channel.name}")
        else:
            print(f"📍 Channel: {message.channel.name}")

        print("---" * 20)

    # Process commands
    await bot.process_commands(message)


@bot.event
async def on_message_delete(message: Message):
    """Event triggered when a message is deleted"""
    # Don't log bot message deletions
    if message.author.bot:
        return

    # Only process deletions from text channels, threads, forum channels, and announcement channels
    if isinstance(
        message.channel,
        (
            discord.TextChannel,
            discord.Thread,
            discord.ForumChannel,
        ),
    ):
        print(f"🗑️ Message deleted: {message.content}")
        print(f"👤 Author: {message.author.name} (ID: {message.author.id})")
        print(f"🏠 Guild: {message.guild.name}")

        if isinstance(message.channel, discord.Thread):
            print(f"🧵 Thread: {message.channel.name}")
            if hasattr(message.channel.parent, "name"):
                print(f"📍 Parent Channel: {message.channel.parent.name}")
        elif isinstance(message.channel, discord.ForumChannel):
            print(f"🗂️ Forum Channel: {message.channel.name}")
        else:
            print(f"📍 Channel: {message.channel.name}")

        print("---" * 20)


# Simple command for testing
@bot.command(name="ping")
async def ping(ctx):
    """Simple ping command"""
    await ctx.send(f"Pong! Latency: {round(bot.latency * 1000)}ms")
    print(f"🏓 Ping command used by {ctx.author.name}")


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ Error: DISCORD_TOKEN not found in environment variables!")
        print("Please set your Discord bot token in the .env file")
        exit(1)

    print("🚀 Starting Discord bot...")
    bot.run(token)

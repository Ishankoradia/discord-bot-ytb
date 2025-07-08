import discord
from discord.ext import commands
from discord.message import Message
from discord.reaction import Reaction
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
intents.reactions = True

# Enable message cache to help with reaction remove events
bot = commands.Bot(command_prefix="!", intents=intents, max_messages=10000)


@bot.event
async def on_ready():
    """Event triggered when the bot is ready"""
    print(f"🤖 Bot is ready! Logged in as {bot.user.name} (ID: {bot.user.id})")
    print(f"📊 Connected to {len(bot.guilds)} servers")
    print(f"🔧 Intents enabled: {bot.intents}")
    print(f"📋 Reactions intent: {bot.intents.reactions}")
    print("---" * 20)


@bot.event
async def on_member_join(member):
    """Event triggered when a new member joins the server"""
    print(f"👋 New member joined: {member.name} (ID: {member.id})")
    print(f"🏠 Guild: {member.guild.name}")
    print(f"📅 Account created: {member.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔢 Member count: {member.guild.member_count}")

    # Try to find a welcome channel (common names)
    welcome_channel = None
    welcome_channel_names = ["welcome", "general", "lobby", "main", "chat"]

    for channel_name in welcome_channel_names:
        channel = discord.utils.get(member.guild.text_channels, name=channel_name)
        if channel:
            welcome_channel = channel
            print(f"📍 Found welcome channel: {channel.name}")
            break

    if welcome_channel:
        import random

        # Random welcome messages
        welcome_messages = [
            f"Welcome to {member.guild.name}, {member.mention}! 👋 We're glad you're here!",
            f"Hey there {member.mention}! 🎉 Welcome to our awesome community!",
            f"🌟 Welcome {member.mention}! Hope you enjoy your time in {member.guild.name}!",
            f"Hello {member.mention}! 👋 Welcome to the server! Feel free to introduce yourself!",
            f"🎊 {member.mention} just joined! Welcome to {member.guild.name}!",
            f"Welcome aboard {member.mention}! 🚀 You're now part of our community!",
            f"Hey {member.mention}! 😊 Welcome to {member.guild.name}! Make yourself at home!",
            f"🎈 A warm welcome to {member.mention}! We're excited to have you here!",
        ]

        # Pick a random welcome message
        welcome_message = random.choice(welcome_messages)

        try:
            await welcome_channel.send(welcome_message)
            print(f"🤖 Sent welcome message: {welcome_message}")
        except discord.Forbidden:
            print("❌ No permission to send welcome message")
        except Exception as e:
            print(f"❌ Error sending welcome message: {e}")
    else:
        print("❌ No suitable welcome channel found")

    print("---" * 20)


@bot.event
async def on_member_remove(member):
    """Event triggered when a member leaves the server"""
    print(f"👋 Member left: {member.name} (ID: {member.id})")
    print(f"🏠 Guild: {member.guild.name}")
    print(f"🔢 Member count: {member.guild.member_count}")

    # Try to find a goodbye channel (common names)
    goodbye_channel = None
    goodbye_channel_names = ["goodbye", "farewell", "general", "lobby", "main", "chat"]

    for channel_name in goodbye_channel_names:
        channel = discord.utils.get(member.guild.text_channels, name=channel_name)
        if channel:
            goodbye_channel = channel
            print(f"📍 Found goodbye channel: {channel.name}")
            break

    if goodbye_channel:
        import random

        # Random goodbye messages
        goodbye_messages = [
            f"Goodbye {member.name}! 👋 Thanks for being part of our community!",
            f"Farewell {member.name}! 🌟 Hope to see you again someday!",
            f"See you later {member.name}! 👋 You'll be missed!",
            f"{member.name} has left the server. Thanks for the memories! 💫",
            f"Goodbye {member.name}! 🚪 The door is always open if you want to return!",
            f"Farewell {member.name}! 👋 Wishing you all the best!",
            f"{member.name} just left. Thanks for being awesome! ✨",
        ]

        # Pick a random goodbye message
        goodbye_message = random.choice(goodbye_messages)

        try:
            await goodbye_channel.send(goodbye_message)
            print(f"🤖 Sent goodbye message: {goodbye_message}")
        except discord.Forbidden:
            print("❌ No permission to send goodbye message")
        except Exception as e:
            print(f"❌ Error sending goodbye message: {e}")
    else:
        print("❌ No suitable goodbye channel found")

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

        # Check if message is in "questions" channel
        if message.channel.name.lower() == "questions":
            print(f"❓ Message in questions channel detected!")
            # Handle questions channel message (create thread)
            await handle_questions_channel(message)

        # Check if the bot is mentioned in the message
        if bot.user in message.mentions:
            print(f"🏷️ Bot was mentioned!")
            print(f"🔗 Mention by: {message.author.name}")
            print(f"📄 Message with mention: {message.content}")

            # You can also check for specific mention patterns
            if message.content.startswith(
                f"<@{bot.user.id}>"
            ) or message.content.startswith(f"<@!{bot.user.id}>"):
                print(f"💬 Bot was mentioned at the start of the message!")

            # Check if it's a reply that mentions the bot
            if message.reference:
                print(f"💬 Bot mentioned in a reply!")

            # Handle the mention (respond to it)
            await handle_bot_mention(message)

        # Check if this message is a reply to another message
        if message.reference:
            print(f"💬 This is a reply!")
            print(f"🔗 Reply to message ID: {message.reference.message_id}")

            # Get the original message being replied to
            try:
                original_message = await message.channel.fetch_message(
                    message.reference.message_id
                )
                print(f"📄 Original message: {original_message.content}")
                print(f"👤 Original author: {original_message.author.name}")
            except discord.NotFound:
                print("❌ Original message not found (might be deleted)")
            except discord.Forbidden:
                print("❌ No permission to fetch the original message")

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


@bot.event
async def on_reaction_add(reaction: Reaction, user):
    """Event triggered when a reaction is added to a message"""
    print(f"🔍 DEBUG: Reaction event triggered!")
    print(f"🔍 DEBUG: User: {user.name}, Bot: {user.bot}")
    print(f"🔍 DEBUG: Channel type: {type(reaction.message.channel)}")
    print(
        f"🔍 DEBUG: Guild: {reaction.message.guild.name if reaction.message.guild else 'DM'}"
    )

    # Don't log bot reactions
    if user.bot:
        return

    # Only process reactions from text channels, threads, forum channels, and announcement channels
    if isinstance(
        reaction.message.channel,
        (
            discord.TextChannel,
            discord.Thread,
            discord.ForumChannel,
        ),
    ):
        print(f"👍 Reaction added: {reaction.emoji}")
        print(f"👤 User: {user.name} (ID: {user.id})")
        print(f"📝 Message: {reaction.message.content}")
        print(f"✍️ Original Author: {reaction.message.author.name}")
        print(f"🏠 Guild: {reaction.message.guild.name}")

        if isinstance(reaction.message.channel, discord.Thread):
            print(f"🧵 Thread: {reaction.message.channel.name}")
            if hasattr(reaction.message.channel.parent, "name"):
                print(f"📍 Parent Channel: {reaction.message.channel.parent.name}")
        elif isinstance(reaction.message.channel, discord.ForumChannel):
            print(f"🗂️ Forum Channel: {reaction.message.channel.name}")
        else:
            print(f"📍 Channel: {reaction.message.channel.name}")

        print("---" * 20)


@bot.event
async def on_reaction_remove(reaction: Reaction, user):
    """Event triggered when a reaction is removed from a message"""
    print(f"🔍 DEBUG: Reaction REMOVE event triggered!")
    print(f"🔍 DEBUG: User: {user.name}, Bot: {user.bot}")
    print(f"🔍 DEBUG: Channel type: {type(reaction.message.channel)}")
    print(
        f"🔍 DEBUG: Guild: {reaction.message.guild.name if reaction.message.guild else 'DM'}"
    )

    # Don't log bot reaction removals
    if user.bot:
        return

    # Only process reaction removals from text channels, threads, forum channels, and announcement channels
    if isinstance(
        reaction.message.channel,
        (
            discord.TextChannel,
            discord.Thread,
            discord.ForumChannel,
        ),
    ):
        print(f"👎 Reaction removed: {reaction.emoji}")
        print(f"👤 User: {user.name} (ID: {user.id})")
        print(f"📝 Message: {reaction.message.content}")
        print(f"✍️ Original Author: {reaction.message.author.name}")
        print(f"🏠 Guild: {reaction.message.guild.name}")

        if isinstance(reaction.message.channel, discord.Thread):
            print(f"🧵 Thread: {reaction.message.channel.name}")
            if hasattr(reaction.message.channel.parent, "name"):
                print(f"📍 Parent Channel: {reaction.message.channel.parent.name}")
        elif isinstance(reaction.message.channel, discord.ForumChannel):
            print(f"🗂️ Forum Channel: {reaction.message.channel.name}")
        else:
            print(f"📍 Channel: {reaction.message.channel.name}")

        print("---" * 20)


@bot.event
async def on_raw_reaction_remove(payload):
    """Event triggered when a reaction is removed (works even if message isn't cached)"""
    print(f"🔍 DEBUG: RAW Reaction REMOVE event triggered!")
    print(f"🔍 DEBUG: User ID: {payload.user_id}")
    print(f"🔍 DEBUG: Message ID: {payload.message_id}")
    print(f"🔍 DEBUG: Channel ID: {payload.channel_id}")
    print(f"🔍 DEBUG: Guild ID: {payload.guild_id}")
    print(f"🔍 DEBUG: Emoji: {payload.emoji}")

    # Don't log bot reaction removals
    if payload.user_id == bot.user.id:
        return

    # Get the guild and channel
    guild = bot.get_guild(payload.guild_id)
    if not guild:
        print("❌ Guild not found")
        return

    channel = guild.get_channel(payload.channel_id)
    if not channel:
        print("❌ Channel not found")
        return

    # Get the user who removed the reaction
    user = guild.get_member(payload.user_id)
    if not user:
        print("❌ User not found")
        return

    # Only process reactions from text channels, threads, forum channels
    if isinstance(channel, (discord.TextChannel, discord.Thread, discord.ForumChannel)):
        print(f"👎 RAW Reaction removed: {payload.emoji}")
        print(f"👤 User: {user.name} (ID: {user.id})")
        print(f"📍 Channel: {channel.name}")
        print(f"🏠 Guild: {guild.name}")

        # Try to get the message (might fail if not cached)
        try:
            message = await channel.fetch_message(payload.message_id)
            print(f"📝 Message: {message.content}")
            print(f"✍️ Original Author: {message.author.name}")
        except discord.NotFound:
            print("❌ Message not found (might be deleted)")
        except discord.Forbidden:
            print("❌ No permission to fetch the message")

        print("---" * 20)


# Simple command for testing
@bot.command(name="ping")
async def ping(ctx):
    """Simple ping command"""
    await ctx.send(f"Pong! Latency: {round(bot.latency * 1000)}ms")
    print(f"🏓 Ping command used by {ctx.author.name}")


@bot.command(name="checkperms")
async def check_permissions(ctx):
    """Check bot permissions in current channel"""
    if ctx.guild:
        bot_member = ctx.guild.get_member(bot.user.id)
        if bot_member:
            perms = bot_member.permissions_in(ctx.channel)
            embed = discord.Embed(title="Bot Permissions", color=0x00FF00)
            embed.add_field(
                name="Read Messages", value=perms.read_messages, inline=True
            )
            embed.add_field(
                name="Send Messages", value=perms.send_messages, inline=True
            )
            embed.add_field(
                name="Add Reactions", value=perms.add_reactions, inline=True
            )
            embed.add_field(
                name="Read Message History",
                value=perms.read_message_history,
                inline=True,
            )
            embed.add_field(
                name="Use External Emojis", value=perms.use_external_emojis, inline=True
            )
            embed.add_field(
                name="Manage Messages", value=perms.manage_messages, inline=True
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Bot member not found in guild")
    else:
        await ctx.send("❌ This command can only be used in a server")


@bot.event
async def on_mention():
    """Handle bot mentions - this will be triggered from on_message"""
    pass


async def handle_questions_channel(message: Message):
    """Handle messages in the questions channel by creating a thread"""
    import random

    # Random thread titles for questions
    thread_titles = [
        f"❓ {message.author.name}'s Question",
        f"🤔 Help Request - {message.author.name}",
        f"💭 Question from {message.author.display_name}",
        f"🔍 {message.author.name} needs help",
        f"❓ Discussion with {message.author.name}",
        f"🆘 Support for {message.author.display_name}",
        f"💬 {message.author.name}'s Thread",
        f"🧠 Question Time - {message.author.name}",
        f"🤝 Helping {message.author.display_name}",
        f"❓ {message.author.name}'s Support Thread",
    ]

    # Pick a random thread title
    thread_title = random.choice(thread_titles)

    try:
        # Create a new thread from the message
        thread = await message.create_thread(name=thread_title)

        # Random responses for questions channel
        responses = [
            f"Hi {message.author.mention}! 👋 I've created this thread for your question. Let's discuss it here!",
            f"Hello {message.author.mention}! 🤔 I saw your question and made a thread so we can help you properly!",
            f"Hey {message.author.mention}! ❓ This thread is dedicated to answering your question. Fire away!",
            f"Welcome {message.author.mention}! 🆘 I've set up this space for your support request. How can we help?",
            f"Hi there {message.author.mention}! 💭 Let's dive into your question in this dedicated thread!",
            f"Hello {message.author.mention}! 🔍 I've created a focused discussion space for your question!",
        ]

        # Pick a random response
        response = random.choice(responses)

        # Send the response in the new thread
        await thread.send(response)

        print(f"🧵 Created questions thread '{thread_title}' for {message.author.name}")
        print(f"🤖 Bot responded in questions thread: {response}")

    except discord.Forbidden:
        # If we can't create a thread, fall back to regular reply
        print("❌ Cannot create thread in questions channel - insufficient permissions")
        fallback_response = f"Hi {message.author.mention}! 👋 I'd love to create a thread for your question, but I don't have permission to do so."
        await message.reply(fallback_response)
        print(f"🤖 Bot replied with fallback in questions: {fallback_response}")
    except Exception as e:
        print(f"❌ Error creating thread in questions channel: {e}")
        # Fallback to regular reply
        fallback_response = f"Hi {message.author.mention}! 👋 I see your question! Something went wrong creating a thread, but I'm here to help!"
        await message.reply(fallback_response)
        print(f"🤖 Bot replied with fallback in questions: {fallback_response}")


async def handle_bot_mention(message: Message):
    """Handle when the bot is mentioned"""
    import random

    # Random thread titles
    thread_titles = [
        f"Chat with {message.author.name}",
        f"Discussion with {message.author.display_name}",
        f"{message.author.name}'s Help Thread",
        f"Conversation - {message.author.name}",
        f"Support Thread for {message.author.name}",
        f"Chat Room - {message.author.display_name}",
        f"{message.author.name}'s Discussion",
        f"Help Desk - {message.author.name}",
        f"Thread for {message.author.display_name}",
        f"Private Chat with {message.author.name}",
    ]

    # Pick a random thread title
    thread_title = random.choice(thread_titles)

    try:
        # Create a new thread from the message
        thread = await message.create_thread(name=thread_title)

        # Random responses to send in the thread
        responses = [
            f"Hey {message.author.mention}! 👋 I've created this thread for our conversation!",
            f"Hello there, {message.author.mention}! How can I help you in this thread?",
            f"You called, {message.author.mention}? 🤖 Let's chat here!",
            f"What's up, {message.author.mention}? 😊 This is our private discussion space!",
            f"Hi {message.author.mention}! I've made a thread just for us to talk! 💬",
        ]

        # Pick a random response
        response = random.choice(responses)

        # Send the response in the new thread (as a reply to the original message)
        await thread.send(response)

        print(f"🧵 Created thread '{thread_title}' for {message.author.name}")
        print(f"🤖 Bot responded in thread: {response}")

    except discord.Forbidden:
        # If we can't create a thread, fall back to regular reply
        print("❌ Cannot create thread - insufficient permissions")
        fallback_response = f"Hey {message.author.mention}! 👋 I'd love to create a thread for us, but I don't have permission to do so."
        await message.reply(fallback_response)
        print(f"🤖 Bot replied with fallback: {fallback_response}")
    except Exception as e:
        print(f"❌ Error creating thread: {e}")
        # Fallback to regular reply
        fallback_response = f"Hey {message.author.mention}! 👋 Something went wrong, but I'm here to help!"
        await message.reply(fallback_response)
        print(f"🤖 Bot replied with fallback: {fallback_response}")


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ Error: DISCORD_TOKEN not found in environment variables!")
        print("Please set your Discord bot token in the .env file")
        exit(1)

    print("🚀 Starting Discord bot...")
    bot.run(token)

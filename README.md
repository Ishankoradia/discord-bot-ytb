# Discord Bot Event Monitor

A Discord bot built with discord.py that monitors and prints various Discord events to the console.

## Features

The bot monitors and prints the following Discord events:
- 🤖 Bot ready status
- 📝 Messages (sent, edited, deleted)
- 👤 Member joins/leaves
- 🏠 Guild joins/leaves
- 👍 Reactions (added/removed)
- 🔊 Voice state changes
- ❗ Error events

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section
4. Click "Reset Token" to get your bot token
5. Copy the token

### 3. Configure Environment

1. Open the `.env` file
2. Replace `your_bot_token_here` with your actual bot token:
   ```
   DISCORD_TOKEN=your_actual_bot_token_here
   ```

### 4. Bot Permissions

When inviting your bot to a server, make sure it has these permissions:
- Read Messages
- Send Messages
- Read Message History
- Add Reactions
- View Channels
- Connect (for voice events)

### 5. Run the Bot

```bash
python bot.py
```

## Commands

The bot includes a few simple commands:
- `!ping` - Check bot latency
- `!info` - Display bot information

## Event Monitoring

Once running, the bot will print detailed information about Discord events to the console:

```
🤖 Bot is ready! Logged in as YourBot (ID: 123456789)
📊 Connected to 1 servers
------------------------------------------------------------
📝 Message: Hello world!
👤 Author: Username (ID: 987654321)
🏠 Guild: My Server
📍 Channel: general
------------------------------------------------------------
```

## File Structure

```
discord-bot-ytb/
├── bot.py              # Main bot code
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (bot token)
└── README.md          # This file
```

## Security Note

Never commit your `.env` file or share your bot token publicly!

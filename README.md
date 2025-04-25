# Discord Bot

A Discord bot that responds to user commands and provides basic functionality.

## Features

- Mention-based command system
- Ping command to check bot latency
- Help command to list available commands
- Configurable logging
- Secure token handling

## Prerequisites

- Python 3.8 or higher
- Discord Bot Token
- Discord.py library
- python-dotenv library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/discord-bot.git
cd discord-bot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
```

5. Edit the `.env` file with your Discord bot token:
```env
DISCORD_TOKEN=your_discord_bot_token_here
```

## Configuration

The bot can be configured through environment variables in the `.env` file:

- `DISCORD_TOKEN`: Your Discord bot token (required)
- `BOT_PREFIX`: Command prefix (default: '!t')
- `LOG_LEVEL`: Logging level (default: 'INFO')
- `LOG_FILE`: Log file name (default: 'bot.log')

## Usage

1. Start the bot:
```bash
python -m discord_bot.bot
```

2. In Discord, use these commands:
- `@BotName ping` - Check bot latency
- `@BotName help` - Show available commands

## Security

- Never commit your `.env` file
- Keep your Discord bot token secure
- The `.env.example` file shows required variables without actual values

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
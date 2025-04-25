# Discord Bot

A Discord bot that responds to user commands and provides basic functionality, including Truth Social integration.

## Features

- Mention-based command system
- Ping command to check bot latency
- Help command to list available commands
- Configurable logging
- Secure token handling
- Truth Social integration via Apify
  - User profile lookup
  - Post fetching
  - Engagement metrics

## Prerequisites

- Python 3.8 or higher
- Discord Bot Token
- Apify API Token
- Discord.py library
- python-dotenv library
- apify-client library

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

5. Edit the `.env` file with your tokens:
```env
# Discord Configuration
DISCORD_TOKEN=your_discord_bot_token_here
BOT_PREFIX=!t
LOG_LEVEL=INFO
LOG_FILE=bot.log

# Apify Configuration
APIFY_API_TOKEN=your_apify_api_token_here
APIFY_ACTOR_ID=muhammetakkurtt/truth-social-scraper
```

## Configuration

The bot can be configured through environment variables in the `.env` file:

### Discord Configuration
- `DISCORD_TOKEN`: Your Discord bot token (required)
- `BOT_PREFIX`: Command prefix (default: '!t')
- `LOG_LEVEL`: Logging level (default: 'INFO')
- `LOG_FILE`: Log file name (default: 'bot.log')

### Apify Configuration
- `APIFY_API_TOKEN`: Your Apify API token (required for Truth Social integration)
- `APIFY_ACTOR_ID`: The Apify actor ID for Truth Social scraping (default: muhammetakkurtt/truth-social-scraper)

## Usage

1. Start the bot:
```bash
python -m discord_bot.bot
```

2. In Discord, use these commands:
- `@BotName ping` - Check bot latency
- `@BotName help` - Show available commands
- `@BotName truth profile @username` - Get Truth Social profile
- `@BotName truth posts @username` - Get recent Truth Social posts

## Security

- Never commit your `.env` file
- Keep your Discord bot token and Apify API token secure
- The `.env.example` file shows required variables without actual values
- API tokens should be rotated if exposed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
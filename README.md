# Discord Truth Social Bot

A Discord bot that integrates with Truth Social to fetch and monitor posts.

## Features

- Fetch user profiles
- Filter posts by keywords and date range
- Monitor posts for specific keywords
- Automatic notifications for new matching posts

## Commands

### Profile Information
- `!ttruth-profile @username` - View a user's profile information

### Post Filtering
- `!tfilter-posts @username [keywords] [days]` - Filter posts by keywords and date range
  - Use quotes for phrases: `!tfilter-posts @user "election fraud" 7`
  - Or separate keywords: `!tfilter-posts @user election fraud 7`
  - Default to 7 days if not specified
  - Maximum 30 days lookback period
  - Maximum 5 results per search

### Post Monitoring
- `!tmonitor-posts @username keyword` - Start monitoring for posts containing a keyword
  - Example: `!tmonitor-posts @realDonaldTrump election`
  - Checks every 5 minutes for new posts
  - Sends notifications when matching posts are found
- `!tstop-monitoring` - Stop monitoring posts
- `!tmonitoring-status` - Check current monitoring status

### Help
- `!thelp` - Show all commands
- `!thelp <command>` - Show detailed help for a specific command

For detailed examples and usage scenarios, see the [Usage Guide](USAGE.md).

## Rate Limits
- Maximum 5 results per search
- 30 second cooldown between searches
- Maximum 20 searches per hour
- Maximum 30 days lookback period
- One active monitoring configuration at a time

## Setup Guide

### Prerequisites
- Python 3.8+ (3.13+ recommended)
- Discord account with developer access
- Apify account (for Truth Social API access)

### Discord Bot Setup
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and name your bot
3. Navigate to the "Bot" tab
4. Click "Add Bot" and confirm
5. Under the "Privileged Gateway Intents" section, enable:
   - Message Content Intent
   - Server Members Intent
   - Presence Intent
6. Copy your bot token (you'll need this for the .env file)
7. Go to the "OAuth2" tab, then "URL Generator"
8. Select scopes: `bot` and `applications.commands`
9. Select bot permissions: 
   - Read Messages/View Channels
   - Send Messages
   - Embed Links
   - Read Message History
10. Copy the generated URL and paste it into your browser to add the bot to your server

### Apify Setup
1. Create an account at [Apify](https://apify.com/)
2. Go to your account settings and find your API token
3. Copy your API token (you'll need this for the .env file)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/discord-truth-social-bot.git
   cd discord-truth-social-bot
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   BOT_PREFIX=!t
   APIFY_API_TOKEN=your_apify_api_token
   ```

5. Initialize the database:
   ```bash
   # The database will be created automatically on first run
   # No manual setup required
   ```

6. Run the bot:
   ```bash
   # Using module syntax (works on all platforms)
   python -m discord_bot.bot
   
   # Windows Command Prompt
   cd C:\path\to\discord-truth-social-bot
   python -m discord_bot.bot
   
   # To keep the bot running after closing the terminal
   # Using start command (Windows)
   start /min python -m discord_bot.bot
   
   # Using nohup (Linux/macOS)
   nohup python -m discord_bot.bot &
   ```

## Development and Testing

### Running Tests
The project includes a comprehensive test suite using pytest:

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_truth_posts.py

# Run tests with coverage report
python -m pytest --cov=discord_bot.commands tests/
```

### Project Structure
```
discord-truth-social-bot/
├── discord_bot/              # Main bot code
│   ├── __init__.py
│   ├── bot.py                # Bot initialization
│   ├── config.py             # Configuration loader
│   ├── database.py           # Database operations
│   └── commands/             # Command implementations
│       ├── __init__.py
│       ├── filter_posts.py
│       ├── help.py
│       ├── monitor_posts.py
│       ├── truth_posts.py
│       └── truth_profile.py
├── truth_social/             # Truth Social API integration
│   ├── __init__.py
│   └── client.py
├── tests/                    # Test suite
├── data/                     # Local database storage
├── requirements.txt          # Python dependencies
└── .env                      # Environment variables
```

## Documentation

- [Setup Guide](#setup-guide) - Instructions for installing and configuring the bot
- [Usage Guide](USAGE.md) - Detailed examples and common workflows
- [API Integration](#api-integration) - Information about the Truth Social API
- [Troubleshooting](#troubleshooting) - Solutions for common issues

## API Integration

This bot uses the Apify platform to access Truth Social data. The integration works as follows:

1. The bot sends requests to Apify's REST API
2. Apify runs a web scraper to extract data from Truth Social
3. The scraped data is processed and returned to the bot
4. The bot formats and displays the information in Discord

For more information about the Apify platform, visit their [documentation](https://docs.apify.com/).

## Troubleshooting

### Common Issues

#### Bot Not Responding to Commands
- Verify the bot is online in Discord
- Check if you're using the correct prefix (default: `!t`)
- Ensure the bot has proper permissions in the Discord channel
- Check bot.log for error messages

#### API Rate Limiting
- The Truth Social API has rate limits
- Use the cooldown features to avoid hitting rate limits
- If you consistently hit rate limits, consider upgrading your Apify plan

#### Database Errors
- If you encounter database errors, try deleting the `data/database.db` file and restart the bot
- Make sure the `data` directory has write permissions

#### Command Errors
- Use `!thelp <command>` to verify the correct command syntax
- Check for proper formatting when using quotes or special characters
- See the [Usage Guide](USAGE.md) for examples of correct command usage

### Logs
- Check the `bot.log` file for error messages
- More detailed logs can be found in the `logs/` directory

## Requirements
- Python 3.8+ (3.13+ recommended)
- discord.py==2.3.2
- python-dotenv==1.0.0
- requests==2.31.0
- aiohttp==3.9.1
- python-dateutil==2.8.2
- apify-client==1.6.1
- pytest==8.0.0 (for development)
- pytest-asyncio==0.23.5 (for development)

## License
MIT 
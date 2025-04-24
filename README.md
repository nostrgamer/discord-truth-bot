# Discord Truth Social Bot

A Discord bot that monitors and forwards posts from Truth Social to Discord channels.

## Features
- Monitors Truth Social for new posts
- Forwards posts to specified Discord channels
- Configurable settings
- Error handling and logging

## Project Structure
```
discord-truth-bot/
├── bot.py              # Main bot file
├── commands/           # Bot commands
│   └── ping.py        # Example ping command
├── .env.example       # Environment variables template
├── requirements.txt   # Python dependencies
└── README.md         # Project documentation
```

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your Discord bot token
4. Run the bot: `python bot.py`

## Configuration
Create a `.env` file with the following variables:
```
DISCORD_TOKEN=your_discord_bot_token
LOG_LEVEL=INFO
LOG_FILE=bot.log
```

## Available Commands
- `!ping` - Check the bot's latency

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details 
# Discord Truth Social Bot

A Discord bot that integrates with Truth Social to fetch and monitor posts.

## Features

- Fetch user profiles
- Filter posts by keywords and date range
- Monitor posts for specific keywords
- Automatic notifications for new matching posts

## Commands

### Profile Information
- `!tprofile @username` - View a user's profile information

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

## Rate Limits
- Maximum 5 results per search
- 30 second cooldown between searches
- Maximum 20 searches per hour
- Maximum 30 days lookback period
- One active monitoring configuration at a time

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   BOT_PREFIX=!t
   APIFY_API_TOKEN=your_apify_api_token
   ```
4. Run the bot:
   ```bash
   python -m discord_bot.bot
   ```

## Requirements
- Python 3.8+
- discord.py
- python-dotenv
- apify-client

## License
MIT 
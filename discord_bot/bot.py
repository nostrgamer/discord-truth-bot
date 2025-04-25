import os
import discord
import logging
import asyncio
from dotenv import load_dotenv
from .config import config
from discord.ext import commands

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = os.getenv("BOT_PREFIX", "!t")

# Bot configuration
class TruthBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix=BOT_PREFIX,
            intents=intents,
            help_command=None
        )
        
    async def setup_hook(self):
        # Load command cogs
        await self.load_extension("discord_bot.commands.truth_profile")
        await self.load_extension("discord_bot.commands.truth_posts")
        
    async def on_ready(self):
        """Called when the bot is ready and connected to Discord."""
        config.logger.info(f'Logged in as {self.user.name}')
        config.logger.info(f'Bot ID: {self.user.id}')
        config.logger.info('------')
        # Print all servers the bot is in
        for guild in self.guilds:
            config.logger.info(f'Bot is in server: {guild.name}')
            # Send a message to each server with instructions
            try:
                channel = guild.system_channel or next((c for c in guild.text_channels if c.permissions_for(guild.me).send_messages), None)
                if channel:
                    await channel.send(
                        f"**Truth Social Bot is online!**\n"
                        f"Available commands:\n"
                        f"`{BOT_PREFIX}ping` - Check bot latency\n"
                        f"`{BOT_PREFIX}help` - Show this help message\n"
                        f"`{BOT_PREFIX}truth-profile @username` - Get Truth Social profile\n"
                        f"`{BOT_PREFIX}truth-posts @username` - Get 5 most recent posts\n\n"
                        f"Examples:\n"
                        f"`{BOT_PREFIX}truth-profile @realDonaldTrump` - Get profile\n"
                        f"`{BOT_PREFIX}truth-posts @realDonaldTrump` - Get 5 recent posts"
                    )
            except Exception as e:
                logger.error(f"Could not send message to {guild.name}: {e}")

    async def on_message(self, message):
        """Handle all messages."""
        # Don't process commands if the message is from the bot itself
        if message.author == self.user:
            return
            
        # Process commands
        await self.process_commands(message)

def main():
    bot = TruthBot()
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main() 
import os
import discord
import logging
import asyncio
from dotenv import load_dotenv
from .config import config
from discord.ext import commands

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='logs/bot.log'
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
        await self.load_extension("discord_bot.commands.filter_posts")
        await self.load_extension("discord_bot.commands.monitor_posts")
        await self.load_extension("discord_bot.commands.help")
        
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
                    embed = discord.Embed(
                        title="Truth Social Bot",
                        description="Thanks for adding me! Here are the available commands:",
                        color=discord.Color.blue()
                    )
                    
                    # Add command information
                    embed.add_field(
                        name="Profile Information",
                        value=f"`{BOT_PREFIX}profile @username` - View a user's profile information",
                        inline=False
                    )
                    
                    embed.add_field(
                        name="Post Filtering",
                        value=f"`{BOT_PREFIX}filter-posts @username [keywords] [days]` - Filter posts by keywords and date range\n"
                              f"• Use quotes for phrases: `{BOT_PREFIX}filter-posts @user \"election fraud\" 7`\n"
                              f"• Or separate keywords: `{BOT_PREFIX}filter-posts @user election fraud 7`",
                        inline=False
                    )
                    
                    embed.add_field(
                        name="Post Monitoring",
                        value=f"`{BOT_PREFIX}monitor-posts @username keyword` - Monitor for new posts containing a keyword\n"
                              f"`{BOT_PREFIX}stop-monitoring` - Stop monitoring posts\n"
                              f"`{BOT_PREFIX}monitoring-status` - Check current monitoring status",
                        inline=False
                    )
                    
                    embed.add_field(
                        name="Help",
                        value=f"`{BOT_PREFIX}help` - Show all commands\n"
                              f"`{BOT_PREFIX}help <command>` - Show detailed help for a specific command",
                        inline=False
                    )
                    
                    # Add footer
                    embed.set_footer(text=f"Use {BOT_PREFIX}help for more information")
                    
                    await channel.send(embed=embed)
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
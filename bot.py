import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Called when the bot is ready and connected to Discord."""
    logger.info(f'Logged in as {bot.user.name} ({bot.user.id})')
    logger.info('------')

@bot.event
async def on_command_error(ctx, error):
    """Global error handler for all commands."""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use !help to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument. Please check the command usage.")
    else:
        logger.error(f'Error in command {ctx.command}: {error}')
        await ctx.send("An error occurred while processing the command.")

# Load commands from the commands directory
async def load_commands():
    """Load all command modules from the commands directory."""
    for filename in os.listdir('./commands'):
        if filename.endswith('.py') and not filename.startswith('_'):
            try:
                await bot.load_extension(f'commands.{filename[:-3]}')
                logger.info(f'Loaded command module: {filename}')
            except Exception as e:
                logger.error(f'Failed to load command module {filename}: {e}')

async def main():
    """Main function to start the bot."""
    async with bot:
        await load_commands()
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 
import os
import discord
import logging
import asyncio
from dotenv import load_dotenv
from .config import config

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
intents.messages = True

class MyBot(discord.Client):
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
                        f"To use commands, mention me like this:\n"
                        f"`<@{self.user.id}> ping` - Check my latency\n"
                        f"`<@{self.user.id}> help` - Show available commands"
                    )
            except Exception as e:
                logger.error(f"Could not send message to {guild.name}: {e}")

    async def on_message(self, message):
        """Handle all messages."""
        config.logger.info(f"Received message: {message.content}")
        
        if message.author == self.user:
            config.logger.info("Ignoring own message")
            return
        
        # Check for both user and role mentions
        bot_mention = f'<@{self.user.id}>'
        role_mention = f'<@&{self.user.id}>'
        
        # Log the mention that was received
        if message.content.startswith('<@'):
            config.logger.info(f"Received mention with ID: {message.content.split('>')[0][2:]}")
        
        if message.content.startswith(bot_mention) or message.content.startswith(role_mention):
            # Remove both types of mentions and get the command
            command = message.content.replace(bot_mention, '').replace(role_mention, '').strip().lower()
            config.logger.info(f"Processing command: {command}")
            
            if command == 'ping':
                config.logger.info("Executing ping command")
                latency = round(self.latency * 1000)
                response = f"🏓 Pong! Latency: {latency}ms"
                await message.channel.send(response)
                config.logger.info("Ping command completed")
            
            elif command == 'help':
                config.logger.info("Executing help command")
                response = (
                    "**Available Commands:**\n"
                    f"`{bot_mention} ping` - Check my latency\n"
                    f"`{bot_mention} help` - Show available commands"
                )
                await message.channel.send(response)
                config.logger.info("Help command completed")

# Create and run the bot
bot = MyBot(intents=intents)
bot.run(config.discord_token) 
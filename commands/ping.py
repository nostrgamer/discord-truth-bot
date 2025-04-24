import discord
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Check the bot's latency."""
        latency = round(self.bot.latency * 1000)
        logger.info(f'Ping command used by {ctx.author.name} (ID: {ctx.author.id})')
        await ctx.send(f'Pong! Latency: {latency}ms')

async def setup(bot):
    """Add the cog to the bot."""
    await bot.add_cog(Ping(bot))
    logger.info('Ping cog loaded') 
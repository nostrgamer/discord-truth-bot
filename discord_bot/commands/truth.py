import discord
from discord.ext import commands
from truth_social.client import TruthSocialClient
from truth_social.config import ApifyConfig
import os

class TruthSocialCommand(commands.Cog):
    """Base class for Truth Social commands."""
    
    def __init__(self, bot):
        self.bot = bot
        self.client = TruthSocialClient(
            ApifyConfig(
                api_token=os.getenv("APIFY_API_TOKEN"),
                actor_id=os.getenv("APIFY_ACTOR_ID", "muhammetakkurtt/truth-social-scraper")
            )
        )
        
    async def cog_before_invoke(self, ctx):
        """Verify the command has the required configuration."""
        if not os.getenv("APIFY_API_TOKEN"):
            await ctx.send("Error: Apify API token not configured. Please check your .env file.")
            return False
        return True 
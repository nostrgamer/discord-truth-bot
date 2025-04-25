import discord
from discord.ext import commands
from .truth import TruthSocialCommand
from datetime import datetime

class TruthProfileCommand(TruthSocialCommand):
    """Command to fetch Truth Social user profiles."""
    
    @commands.command(name="truth-profile")
    async def truth_profile(self, ctx, username: str):
        """Fetch and display a Truth Social user's profile.
        
        Usage: !truth-profile @username
        Example: !truth-profile @realDonaldTrump
        """
        # Remove @ if present
        username = username.lstrip('@')
        
        try:
            # Show typing indicator while fetching
            async with ctx.typing():
                profile = await self.client.get_user_profile(username)
                
                # Create embed
                embed = discord.Embed(
                    title=f"Truth Social Profile: {profile.display_name}",
                    url=f"https://truthsocial.com/@{profile.username}",
                    color=discord.Color.blue()
                )
                
                # Add profile information
                embed.add_field(name="Username", value=f"@{profile.username}", inline=True)
                embed.add_field(name="Verified", value="✅" if profile.is_verified else "❌", inline=True)
                embed.add_field(name="Followers", value=f"{profile.followers_count:,}", inline=True)
                embed.add_field(name="Following", value=f"{profile.following_count:,}", inline=True)
                embed.add_field(name="Posts", value=f"{profile.posts_count:,}", inline=True)
                embed.add_field(name="Joined", value=profile.created_at.strftime("%B %d, %Y"), inline=True)
                
                if profile.bio:
                    embed.add_field(name="Bio", value=profile.bio, inline=False)
                
                # Set footer with timestamp
                embed.set_footer(text=f"Requested by {ctx.author.name}")
                embed.timestamp = datetime.utcnow()
                
                await ctx.send(embed=embed)
                
        except Exception as e:
            await ctx.send(f"Error fetching profile: {str(e)}")

async def setup(bot):
    await bot.add_cog(TruthProfileCommand(bot)) 
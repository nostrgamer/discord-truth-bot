import discord
from discord.ext import commands
from .truth import TruthSocialCommand
from typing import Optional

class ProfileCommand(TruthSocialCommand):
    """Command to fetch and display Truth Social user profile information."""
    
    @commands.command(name="profile")
    async def profile(self, ctx, username: str):
        """Display information about a Truth Social user.
        
        Usage: !profile @username
        Example: !profile @realDonaldTrump
        
        Parameters:
        @username - Required. The Truth Social username to look up
        """
        # Remove @ if present
        username = username.lstrip('@')
        
        try:
            # Show typing indicator while fetching
            async with ctx.typing():
                # Get user profile
                profile = await self.client.get_user_profile(username)
                
                # Create embed
                embed = discord.Embed(
                    title=f"@{profile.username}",
                    description=profile.bio or "No bio available",
                    color=discord.Color.blue()
                )
                
                # Add profile information
                embed.add_field(
                    name="Display Name",
                    value=profile.display_name,
                    inline=True
                )
                embed.add_field(
                    name="Location",
                    value=profile.location or "Not specified",
                    inline=True
                )
                embed.add_field(
                    name="Join Date",
                    value=profile.created_at.strftime("%B %d, %Y"),
                    inline=True
                )
                
                # Add statistics
                embed.add_field(
                    name="Posts",
                    value=f"{profile.posts_count:,}",
                    inline=True
                )
                embed.add_field(
                    name="Following",
                    value=f"{profile.following_count:,}",
                    inline=True
                )
                embed.add_field(
                    name="Followers",
                    value=f"{profile.followers_count:,}",
                    inline=True
                )
                
                # Add profile URL
                embed.add_field(
                    name="Profile URL",
                    value=f"https://truthsocial.com/@{profile.username}",
                    inline=False
                )
                
                # Set footer
                embed.set_footer(text=f"Requested by {ctx.author.name}")
                
                # Set thumbnail if available
                if profile.avatar_url:
                    embed.set_thumbnail(url=profile.avatar_url)
                
                await ctx.send(embed=embed)
                
        except Exception as e:
            await ctx.send(f"Error fetching profile: {str(e)}")

async def setup(bot):
    await bot.add_cog(ProfileCommand(bot)) 
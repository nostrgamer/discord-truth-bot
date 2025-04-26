import discord
from discord.ext import commands
from .truth import TruthSocialCommand
from datetime import datetime

class TruthPostsCommand(TruthSocialCommand):
    """Command to fetch Truth Social user posts."""
    
    @commands.command(name="truth-posts")
    async def truth_posts(self, ctx, username: str):
        """Fetch and display a Truth Social user's recent posts.
        
        Usage: !truth-posts @username
        Example: !truth-posts @realDonaldTrump
        """
        # Remove @ if present
        username = username.lstrip('@')
        
        try:
            # Show typing indicator while fetching
            async with ctx.typing():
                posts = await self.client.get_user_posts(username, limit=5)
                
                # Create embed for each post
                for i, post in enumerate(posts.posts, 1):
                    embed = discord.Embed(
                        title=f"Post {i} by {post.user.display_name}",
                        url=f"https://truthsocial.com/@{post.user.username}/{post.id}",
                        description=post.content,
                        color=discord.Color.blue(),
                        timestamp=post.created_at
                    )
                    
                    # Add engagement metrics
                    embed.add_field(name="Likes", value=f"{post.likes_count:,}", inline=True)
                    embed.add_field(name="Replies", value=f"{post.replies_count:,}", inline=True)
                    embed.add_field(name="Reposts", value=f"{post.reposts_count:,}", inline=True)
                    
                    # Set footer
                    embed.set_footer(text=f"Requested by {ctx.author.name}")
                    
                    await ctx.send(embed=embed)
                    
        except Exception as e:
            await ctx.send(f"Error fetching posts: {str(e)}")

async def setup(bot):
    await bot.add_cog(TruthPostsCommand(bot)) 
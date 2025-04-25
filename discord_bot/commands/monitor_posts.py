import discord
from discord.ext import commands
from .truth import TruthSocialCommand
from ..database import Database
from datetime import datetime, timedelta, timezone
from typing import Optional
import asyncio

class MonitorPostsCommand(TruthSocialCommand):
    """Command to monitor Truth Social posts for specific keywords."""
    
    def __init__(self, bot):
        super().__init__(bot)
        self.db = Database()
        self._monitoring_task = None
        self._check_interval = 300  # 5 minutes in seconds
        
    async def _check_for_new_posts(self):
        """Background task to check for new posts."""
        while True:
            try:
                if not self.db.is_monitoring_active():
                    await asyncio.sleep(self._check_interval)
                    continue
                    
                config = self.db.get_monitoring_config()
                if not config:
                    await asyncio.sleep(self._check_interval)
                    continue
                
                # Get new posts
                posts = await self.client.get_user_posts(config['username'])
                
                # Filter by keyword
                keyword = config['filter_keyword'].lower()
                new_posts = [
                    post for post in posts.posts
                    if keyword in post.content.lower()
                ]
                
                # If we have a last checked post, only show newer ones
                if config['last_post_id']:
                    new_posts = [
                        post for post in new_posts
                        if post.id != config['last_post_id']
                    ]
                
                # Send notifications for new posts
                for post in new_posts:
                    embed = discord.Embed(
                        title=f"New post by {post.author.display_name}",
                        description=post.content,
                        color=discord.Color.green(),
                        timestamp=post.created_at
                    )
                    
                    # Add engagement metrics
                    embed.add_field(name="Likes", value=post.likes_count, inline=True)
                    embed.add_field(name="Replies", value=post.replies_count, inline=True)
                    embed.add_field(name="Reposts", value=post.reposts_count, inline=True)
                    
                    # Add filter info
                    embed.set_footer(text=f"Matching keyword: {config['filter_keyword']}")
                    
                    # Send to all channels where the command was used
                    for channel in self.bot.get_all_channels():
                        if isinstance(channel, discord.TextChannel):
                            await channel.send(embed=embed)
                
                # Update last checked
                if new_posts:
                    self.db.update_last_checked(
                        new_posts[0].id,
                        datetime.now(timezone.utc).isoformat()
                    )
                
            except Exception as e:
                print(f"Error in monitoring task: {str(e)}")
            
            await asyncio.sleep(self._check_interval)
    
    @commands.command(name="monitor-posts")
    async def monitor_posts(self, ctx, username: str, keyword: str):
        """Start monitoring posts for a specific keyword.
        
        Usage: !monitor-posts username keyword
        Example: !monitor-posts realDonaldTrump "election"
        """
        try:
            # Remove @ if present
            username = username.lstrip('@')
            
            # Check if monitoring is already active
            if self.db.is_monitoring_active():
                await ctx.send("Monitoring is already active. Use !stop-monitoring to stop first.")
                return
            
            # Add new monitoring configuration
            self.db.add_monitoring_config(username, keyword)
            
            # Start monitoring task if not already running
            if not self._monitoring_task:
                self._monitoring_task = self.bot.loop.create_task(self._check_for_new_posts())
            
            await ctx.send(
                f"Started monitoring posts from @{username} for keyword: {keyword}\n"
                f"I'll notify you when new matching posts are found!"
            )
            
        except Exception as e:
            await ctx.send(f"Error setting up monitoring: {str(e)}")
    
    @commands.command(name="stop-monitoring")
    async def stop_monitoring(self, ctx):
        """Stop monitoring posts."""
        try:
            if not self.db.is_monitoring_active():
                await ctx.send("No active monitoring to stop.")
                return
            
            self.db.deactivate_monitoring()
            await ctx.send("Monitoring stopped successfully.")
            
        except Exception as e:
            await ctx.send(f"Error stopping monitoring: {str(e)}")
    
    @commands.command(name="monitoring-status")
    async def monitoring_status(self, ctx):
        """Check the current monitoring status."""
        try:
            config = self.db.get_monitoring_config()
            if not config:
                await ctx.send("No active monitoring configuration.")
                return
            
            embed = discord.Embed(
                title="Monitoring Status",
                color=discord.Color.blue()
            )
            
            embed.add_field(name="Username", value=config['username'], inline=True)
            embed.add_field(name="Keyword", value=config['filter_keyword'], inline=True)
            embed.add_field(name="Active", value="Yes", inline=True)
            
            if config['last_checked_timestamp']:
                last_checked = datetime.fromisoformat(config['last_checked_timestamp'])
                embed.add_field(
                    name="Last Checked",
                    value=last_checked.strftime("%Y-%m-%d %H:%M:%S"),
                    inline=False
                )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"Error getting monitoring status: {str(e)}")

async def setup(bot):
    await bot.add_cog(MonitorPostsCommand(bot)) 
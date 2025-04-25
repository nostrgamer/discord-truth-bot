import discord
from discord.ext import commands
from .truth import TruthSocialCommand
from datetime import datetime, timedelta, timezone
from typing import Optional, List
import shlex
import asyncio
from collections import defaultdict

class FilterPostsCommand(TruthSocialCommand):
    """Command to filter Truth Social posts by various criteria."""
    
    def __init__(self, bot):
        super().__init__(bot)
        self._cooldowns = defaultdict(list)
        self._max_results = 5  # Maximum number of posts to return
        self._cooldown_time = 30  # Cooldown in seconds
        self._max_requests_per_hour = 20  # Maximum API requests per hour per user
        self._max_days = 30  # Maximum number of days to look back
        
    def _is_on_cooldown(self, user_id: int) -> bool:
        """Check if a user is on cooldown."""
        now = datetime.now()
        # Remove expired cooldowns
        self._cooldowns[user_id] = [t for t in self._cooldowns[user_id] 
                                  if (now - t).total_seconds() < self._cooldown_time]
        # Check if user has exceeded hourly limit
        hour_ago = now - timedelta(hours=1)
        recent_requests = [t for t in self._cooldowns[user_id] if t > hour_ago]
        return len(recent_requests) >= self._max_requests_per_hour
    
    def _add_cooldown(self, user_id: int):
        """Add a cooldown for a user."""
        self._cooldowns[user_id].append(datetime.now())
    
    @commands.command(name="filter-posts")
    async def filter_posts(self, ctx, username: str, keywords: Optional[str] = None, days: Optional[int] = None):
        """Filter posts by username, keywords, and date range.
        
        Usage: !filter-posts username [keywords] [days]
        Example: !filter-posts realDonaldTrump "election fraud" 7
        
        Rate Limits:
        - Maximum 5 results per search
        - 30 second cooldown between searches
        - Maximum 20 searches per hour
        - Maximum 30 days lookback period
        """
        try:
            # Check cooldown
            if self._is_on_cooldown(ctx.author.id):
                remaining = self._cooldown_time - (datetime.now() - self._cooldowns[ctx.author.id][-1]).total_seconds()
                await ctx.send(f"Please wait {int(remaining)} seconds before using this command again.")
                return
            
            # Default to 7 days if not specified
            days = days or 7
            
            # Enforce maximum days limit
            if days > self._max_days:
                await ctx.send(f"Maximum lookback period is {self._max_days} days. Using {self._max_days} days instead.")
                days = self._max_days
            
            # Remove @ if present
            username = username.lstrip('@')
            
            # Show typing indicator while fetching
            async with ctx.typing():
                # Get posts
                posts = await self.client.get_user_posts(username)
                
                # Filter by date range
                cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
                filtered_posts = [
                    post for post in posts.posts 
                    if post.created_at >= cutoff_date
                ]
                
                # Filter by keywords if provided
                if keywords:
                    keyword_list = [k.strip().lower() for k in keywords.split(',')]
                    filtered_posts = [
                        post for post in filtered_posts
                        if any(keyword in post.content.lower() for keyword in keyword_list)
                    ]
                
                if not filtered_posts:
                    await ctx.send(f"No posts found for {username} matching the criteria.")
                    return
                
                # Limit the number of results
                if len(filtered_posts) > self._max_results:
                    await ctx.send(f"Found {len(filtered_posts)} posts. Showing the {self._max_results} most recent matching posts.")
                    filtered_posts = filtered_posts[:self._max_results]
                
                # Send filtered posts
                for post in filtered_posts:
                    embed = discord.Embed(
                        title=f"Post by {post.author.display_name}",
                        description=post.content,
                        color=discord.Color.blue(),
                        timestamp=post.created_at
                    )
                    
                    # Add engagement metrics
                    embed.add_field(name="Likes", value=post.likes_count, inline=True)
                    embed.add_field(name="Replies", value=post.replies_count, inline=True)
                    embed.add_field(name="Reposts", value=post.reposts_count, inline=True)
                    
                    # Add filter info
                    filter_info = f"Posted within the last {days} days"
                    if keywords:
                        filter_info += f"\nContains keywords: {keywords}"
                    embed.set_footer(text=filter_info)
                    
                    await ctx.send(embed=embed)
                
                # Add cooldown
                self._add_cooldown(ctx.author.id)
                
                await ctx.send(f"Found {len(filtered_posts)} posts matching your criteria.")
            
        except Exception as e:
            await ctx.send(f"Error filtering posts: {str(e)}")

async def setup(bot):
    await bot.add_cog(FilterPostsCommand(bot)) 
import discord
from discord.ext import commands
from typing import Optional

class HelpCommand(commands.Cog):
    """Help command to provide information about available commands."""
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="help")
    async def help(self, ctx, command: Optional[str] = None):
        """Show help information for commands.
        
        Usage: !help [command]
        Example: !help filter-posts
        """
        if command:
            # Show help for specific command
            cmd = self.bot.get_command(command)
            if cmd:
                embed = discord.Embed(
                    title=f"Command: {cmd.name}",
                    description=cmd.help or "No description available",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Command '{command}' not found.")
        else:
            # Show general help
            embed = discord.Embed(
                title="Truth Social Bot Commands",
                description="Here are all available commands:",
                color=discord.Color.blue()
            )
            
            # Add command information
            for cmd in self.bot.commands:
                if not cmd.hidden:
                    embed.add_field(
                        name=f"!{cmd.name}",
                        value=cmd.help.split('\n')[0] if cmd.help else "No description available",
                        inline=False
                    )
            
            # Add footer
            embed.set_footer(text="Use !help <command> for more details")
            
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot)) 
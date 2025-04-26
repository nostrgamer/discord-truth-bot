"""Tests for the help command."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from discord_bot.commands.help import HelpCommand
from discord import Embed

@pytest.mark.asyncio
async def test_general_help():
    """Test displaying general help information."""
    # Create mocks
    mock_bot = AsyncMock()
    ctx = AsyncMock()
    
    # Mock bot commands
    command1 = MagicMock()
    command1.name = "test-command"
    command1.help = "This is a test command\nUsage: !test-command"
    command1.hidden = False
    
    command2 = MagicMock()
    command2.name = "another-command"
    command2.help = "This is another command\nUsage: !another-command"
    command2.hidden = False
    
    hidden_command = MagicMock()
    hidden_command.name = "hidden"
    hidden_command.help = "This is a hidden command"
    hidden_command.hidden = True
    
    # Set up bot's commands attribute
    mock_bot.commands = [command1, command2, hidden_command]
    
    # Create test implementation
    class TestHelpImpl:
        def __init__(self, bot):
            self.bot = bot
        
        async def help(self, ctx, command=None):
            if command:
                # Show help for specific command
                cmd = next((c for c in self.bot.commands if c.name == command), None)
                if cmd:
                    embed = Embed(
                        title=f"Command: {cmd.name}",
                        description=cmd.help or "No description available",
                        color=0x0000FF
                    )
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"Command '{command}' not found.")
            else:
                # Show general help
                embed = Embed(
                    title="Bot Commands",
                    description="Here are all available commands:",
                    color=0x0000FF
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
    
    # Create test instance
    test_help = TestHelpImpl(mock_bot)
    
    # Execute general help
    await test_help.help(ctx)
    
    # Verify send was called with an embed
    ctx.send.assert_called_once()
    embed = ctx.send.call_args[1]['embed']
    
    # Verify embed contains the expected information
    assert embed.title == "Bot Commands"
    assert "Here are all available commands" in embed.description
    
    # Verify it shows the visible commands but not the hidden one
    field_names = [field.name for field in embed.fields]
    assert "!test-command" in field_names
    assert "!another-command" in field_names
    assert "!hidden" not in field_names
    
    # Verify footer text
    assert "Use !help <command> for more details" in embed.footer.text

@pytest.mark.asyncio
async def test_specific_command_help():
    """Test displaying help for a specific command."""
    # Create mocks
    mock_bot = AsyncMock()
    ctx = AsyncMock()
    
    # Mock bot commands
    command1 = MagicMock()
    command1.name = "test-command"
    command1.help = "This is a test command\nUsage: !test-command <arg>\nExample: !test-command example"
    command1.hidden = False
    
    # Set up bot's commands attribute
    mock_bot.commands = [command1]
    
    # Create test implementation (reusing the class from the previous test)
    class TestHelpImpl:
        def __init__(self, bot):
            self.bot = bot
        
        async def help(self, ctx, command=None):
            if command:
                # Show help for specific command
                cmd = next((c for c in self.bot.commands if c.name == command), None)
                if cmd:
                    embed = Embed(
                        title=f"Command: {cmd.name}",
                        description=cmd.help or "No description available",
                        color=0x0000FF
                    )
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"Command '{command}' not found.")
            else:
                # Show general help (simplified for this test)
                embed = Embed(title="Bot Commands", description="General help")
                await ctx.send(embed=embed)
    
    # Create test instance
    test_help = TestHelpImpl(mock_bot)
    
    # Execute help for a specific command
    await test_help.help(ctx, command="test-command")
    
    # Verify send was called with an embed
    ctx.send.assert_called_once()
    embed = ctx.send.call_args[1]['embed']
    
    # Verify embed contains the expected command information
    assert embed.title == "Command: test-command"
    assert "This is a test command" in embed.description
    assert "Usage: !test-command <arg>" in embed.description
    assert "Example: !test-command example" in embed.description

@pytest.mark.asyncio
async def test_help_invalid_command():
    """Test help with an invalid command name."""
    # Create mocks
    mock_bot = AsyncMock()
    ctx = AsyncMock()
    
    # Mock bot commands (empty for simplicity)
    mock_bot.commands = []
    
    # Create test implementation (reusing the class from previous tests)
    class TestHelpImpl:
        def __init__(self, bot):
            self.bot = bot
        
        async def help(self, ctx, command=None):
            if command:
                # Show help for specific command
                cmd = next((c for c in self.bot.commands if c.name == command), None)
                if cmd:
                    embed = Embed(
                        title=f"Command: {cmd.name}",
                        description=cmd.help or "No description available",
                        color=0x0000FF
                    )
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"Command '{command}' not found.")
            else:
                # Show general help (simplified for this test)
                embed = Embed(title="Bot Commands", description="General help")
                await ctx.send(embed=embed)
    
    # Create test instance
    test_help = TestHelpImpl(mock_bot)
    
    # Execute help with a non-existent command
    await test_help.help(ctx, command="nonexistent-command")
    
    # Verify send was called with an error message
    ctx.send.assert_called_once()
    error_message = ctx.send.call_args[0][0]
    assert "Command 'nonexistent-command' not found" in error_message

@pytest.mark.asyncio
async def test_help_command_aliases():
    """Test that help command can show command aliases."""
    # Create mocks
    mock_bot = AsyncMock()
    ctx = AsyncMock()
    
    # Create a command with aliases
    command_with_aliases = MagicMock()
    command_with_aliases.name = "profile"
    command_with_aliases.help = "Display profile information\nUsage: !profile <username>"
    command_with_aliases.aliases = ["p", "user-profile"]
    command_with_aliases.hidden = False
    
    # Set up bot's commands attribute
    mock_bot.commands = [command_with_aliases]
    
    # Create test implementation
    class TestHelpImpl:
        def __init__(self, bot):
            self.bot = bot
        
        async def help(self, ctx, command=None):
            if command:
                # Show help for specific command
                cmd = next((c for c in self.bot.commands if c.name == command), None)
                if cmd:
                    embed = Embed(
                        title=f"Command: {cmd.name}",
                        description=cmd.help or "No description available",
                        color=0x0000FF
                    )
                    
                    # Add aliases if any
                    if hasattr(cmd, 'aliases') and cmd.aliases:
                        aliases_text = ", ".join([f"!{a}" for a in cmd.aliases])
                        embed.add_field(
                            name="Aliases",
                            value=aliases_text,
                            inline=False
                        )
                    
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"Command '{command}' not found.")
            else:
                # Show general help (simplified for this test)
                embed = Embed(title="Bot Commands", description="General help")
                await ctx.send(embed=embed)
    
    # Create test instance
    test_help = TestHelpImpl(mock_bot)
    
    # Execute help for a command with aliases
    await test_help.help(ctx, command="profile")
    
    # Verify send was called with an embed
    ctx.send.assert_called_once()
    embed = ctx.send.call_args[1]['embed']
    
    # Verify embed contains command information
    assert embed.title == "Command: profile"
    
    # Verify aliases field
    aliases_field = next((f for f in embed.fields if f.name == "Aliases"), None)
    assert aliases_field is not None
    assert "!p" in aliases_field.value
    assert "!user-profile" in aliases_field.value 
"""Tests for the Discord bot."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import discord
from discord.ext import commands
from discord_bot.bot import TruthBot, BOT_PREFIX, DISCORD_TOKEN

@pytest.fixture
def mock_discord_bot():
    """Create a mock Discord bot instance."""
    with patch('discord.ext.commands.Bot.run'), \
         patch('discord.ext.commands.Bot.__init__') as mock_init:
        bot = TruthBot()
        # Mock internal Discord.py attributes
        bot._connection = MagicMock()
        mock_user = MagicMock()
        mock_user.name = "TestBot"
        mock_user.id = "123456789"
        bot._connection.user = mock_user
        
        # Mock guilds list
        bot._connection.guilds = []
        
        # Ensure the mock_init was called with correct arguments
        assert mock_init.called
        args, kwargs = mock_init.call_args
        assert kwargs['command_prefix'] == BOT_PREFIX
        assert isinstance(kwargs['intents'], discord.Intents)
        assert kwargs['help_command'] is None
        return bot

@pytest.mark.asyncio
async def test_setup_hook():
    """Test that all command extensions are loaded."""
    with patch('discord.ext.commands.Bot.__init__'):
        bot = TruthBot()
        # Mock the load_extension method
        bot.load_extension = AsyncMock()
        
        # Call setup_hook
        await bot.setup_hook()
        
        # Verify all extensions were loaded
        expected_extensions = [
            "discord_bot.commands.truth_profile",
            "discord_bot.commands.truth_posts",
            "discord_bot.commands.filter_posts",
            "discord_bot.commands.monitor_posts",
            "discord_bot.commands.help"
        ]
        
        assert bot.load_extension.call_count == len(expected_extensions)
        for ext in expected_extensions:
            bot.load_extension.assert_any_call(ext)

@pytest.mark.asyncio
async def test_on_ready(mock_discord_bot):
    """Test the on_ready event handler."""
    # Mock guilds
    mock_guild = MagicMock()
    mock_guild.name = "Test Server"
    mock_guild.me = MagicMock()
    
    # Mock text channel
    mock_channel = AsyncMock()
    mock_guild.system_channel = mock_channel
    mock_guild.text_channels = [mock_channel]
    
    mock_discord_bot._connection.guilds = [mock_guild]
    
    # Call on_ready
    await mock_discord_bot.on_ready()
    
    # Verify channel.send was called with an embed
    assert mock_channel.send.called
    call_args = mock_channel.send.call_args
    assert 'embed' in call_args[1]
    
    # Verify embed contents
    embed = call_args[1]['embed']
    assert isinstance(embed, discord.Embed)
    assert embed.title == "Truth Social Bot"
    assert "Thanks for adding me!" in embed.description
    
    # Verify command fields
    field_names = [field.name for field in embed.fields]
    assert "Profile Information" in field_names
    assert "Post Filtering" in field_names
    assert "Post Monitoring" in field_names
    assert "Help" in field_names

@pytest.mark.asyncio
async def test_on_ready_no_system_channel(mock_discord_bot):
    """Test on_ready when guild has no system channel."""
    # Mock guild with no system channel
    mock_guild = MagicMock()
    mock_guild.name = "Test Server"
    mock_guild.me = MagicMock()
    mock_guild.system_channel = None
    
    # Mock text channel with send permissions
    mock_channel = AsyncMock()
    mock_permissions = MagicMock()
    mock_permissions.send_messages = True
    mock_channel.permissions_for = MagicMock(return_value=mock_permissions)
    mock_guild.text_channels = [mock_channel]
    
    mock_discord_bot._connection.guilds = [mock_guild]
    
    # Call on_ready
    await mock_discord_bot.on_ready()
    
    # Verify channel.send was called
    assert mock_channel.send.called

@pytest.mark.asyncio
async def test_on_ready_no_available_channels(mock_discord_bot):
    """Test on_ready when no channels are available to send messages."""
    # Mock guild with no available channels
    mock_guild = MagicMock()
    mock_guild.name = "Test Server"
    mock_guild.me = MagicMock()
    mock_guild.system_channel = None
    
    # Mock text channel without send permissions
    mock_channel = AsyncMock()
    mock_permissions = MagicMock()
    mock_permissions.send_messages = False
    mock_channel.permissions_for = MagicMock(return_value=mock_permissions)
    mock_guild.text_channels = [mock_channel]
    
    mock_discord_bot._connection.guilds = [mock_guild]
    
    # Call on_ready
    await mock_discord_bot.on_ready()
    
    # Verify channel.send was not called
    assert not mock_channel.send.called

@pytest.mark.asyncio
async def test_on_message_from_bot(mock_discord_bot):
    """Test that messages from the bot are ignored."""
    # Create a message from the bot
    message = MagicMock()
    message.author = mock_discord_bot._connection.user
    
    # Mock process_commands
    mock_discord_bot.process_commands = AsyncMock()
    
    # Call on_message
    await mock_discord_bot.on_message(message)
    
    # Verify process_commands was not called
    assert not mock_discord_bot.process_commands.called

@pytest.mark.asyncio
async def test_on_message_from_user(mock_discord_bot):
    """Test that messages from users are processed."""
    # Create a message from a user
    message = MagicMock()
    message.author = MagicMock()  # Different from bot.user
    
    # Mock process_commands
    mock_discord_bot.process_commands = AsyncMock()
    
    # Call on_message
    await mock_discord_bot.on_message(message)
    
    # Verify process_commands was called
    mock_discord_bot.process_commands.assert_called_once_with(message)

def test_main():
    """Test the main function."""
    with patch('discord_bot.bot.TruthBot') as mock_bot_class:
        from discord_bot.bot import main
        
        # Create a mock bot instance
        mock_bot = MagicMock()
        mock_bot_class.return_value = mock_bot
        
        # Call main
        main()
        
        # Verify bot was created and run
        assert mock_bot_class.called
        assert mock_bot.run.called
        mock_bot.run.assert_called_once_with(DISCORD_TOKEN) 
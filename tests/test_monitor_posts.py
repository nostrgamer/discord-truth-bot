"""Tests for the monitor_posts command."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from datetime import datetime, timezone
import discord
from discord.ext import commands
from discord_bot.commands.monitor_posts import MonitorPostsCommand

@pytest.fixture
def mock_bot():
    """Create a mock bot instance."""
    bot = MagicMock()
    bot.loop = MagicMock()
    bot.loop.create_task = MagicMock()
    return bot

@pytest.fixture
def mock_db():
    """Create a mock database instance."""
    with patch('discord_bot.commands.monitor_posts.Database') as mock_db_class:
        db = MagicMock()
        mock_db_class.return_value = db
        yield db

@pytest.fixture
def command(mock_bot, mock_db):
    """Create a MonitorPostsCommand instance with mocked dependencies."""
    cmd = MonitorPostsCommand(mock_bot)
    # Access the command methods directly from the class
    cmd.monitor_posts = cmd.monitor_posts.callback
    cmd.stop_monitoring = cmd.stop_monitoring.callback
    cmd.monitoring_status = cmd.monitoring_status.callback
    return cmd

@pytest.mark.asyncio
async def test_monitor_posts_start(command, mock_db):
    """Test starting post monitoring."""
    # Create mock context
    ctx = AsyncMock()
    ctx.send = AsyncMock()
    
    # Configure mock database
    mock_db.is_monitoring_active.return_value = False
    mock_db.add_monitoring_config = MagicMock()
    
    # Test the command
    await command.monitor_posts(command, ctx, "test_user", "test_keyword")
    
    # Verify database calls
    mock_db.is_monitoring_active.assert_called_once()
    mock_db.add_monitoring_config.assert_called_once_with("test_user", "test_keyword")
    
    # Verify monitoring task was created
    command.bot.loop.create_task.assert_called_once()
    
    # Verify success message
    ctx.send.assert_called_once()
    success_msg = ctx.send.call_args[0][0]
    assert "Started monitoring posts from @test_user" in success_msg
    assert "test_keyword" in success_msg

@pytest.mark.asyncio
async def test_monitor_posts_already_active(command, mock_db):
    """Test starting monitoring when it's already active."""
    # Create mock context
    ctx = AsyncMock()
    ctx.send = AsyncMock()
    
    # Configure mock database to return active monitoring
    mock_db.is_monitoring_active.return_value = True
    
    # Test the command
    await command.monitor_posts(command, ctx, "test_user", "test_keyword")
    
    # Verify database was checked
    mock_db.is_monitoring_active.assert_called_once()
    
    # Verify add_monitoring_config was not called
    mock_db.add_monitoring_config.assert_not_called()
    
    # Verify error message
    ctx.send.assert_called_once()
    error_msg = ctx.send.call_args[0][0]
    assert "Monitoring is already active" in error_msg

@pytest.mark.asyncio
async def test_stop_monitoring(command, mock_db):
    """Test stopping post monitoring."""
    # Create mock context
    ctx = AsyncMock()
    ctx.send = AsyncMock()
    
    # Configure mock database
    mock_db.is_monitoring_active.return_value = True
    mock_db.deactivate_monitoring = MagicMock()
    
    # Test the command
    await command.stop_monitoring(command, ctx)
    
    # Verify database calls
    mock_db.is_monitoring_active.assert_called_once()
    mock_db.deactivate_monitoring.assert_called_once()
    
    # Verify success message
    ctx.send.assert_called_once()
    success_msg = ctx.send.call_args[0][0]
    assert "Monitoring stopped successfully" in success_msg

@pytest.mark.asyncio
async def test_stop_monitoring_not_active(command, mock_db):
    """Test stopping monitoring when it's not active."""
    # Create mock context
    ctx = AsyncMock()
    ctx.send = AsyncMock()
    
    # Configure mock database
    mock_db.is_monitoring_active.return_value = False
    
    # Test the command
    await command.stop_monitoring(command, ctx)
    
    # Verify database was checked
    mock_db.is_monitoring_active.assert_called_once()
    
    # Verify deactivate_monitoring was not called
    mock_db.deactivate_monitoring.assert_not_called()
    
    # Verify error message
    ctx.send.assert_called_once()
    error_msg = ctx.send.call_args[0][0]
    assert "No active monitoring to stop" in error_msg

@pytest.mark.asyncio
async def test_monitoring_status_active(command, mock_db):
    """Test checking monitoring status when active."""
    # Create mock context
    ctx = AsyncMock()
    ctx.send = AsyncMock()
    
    # Create mock config
    mock_config = {
        'username': 'test_user',
        'filter_keyword': 'test_keyword',
        'last_checked_timestamp': datetime.now(timezone.utc).isoformat()
    }
    
    # Configure mock database
    mock_db.get_monitoring_config.return_value = mock_config
    
    # Test the command
    await command.monitoring_status(command, ctx)
    
    # Verify database call
    mock_db.get_monitoring_config.assert_called_once()
    
    # Verify embed was sent
    ctx.send.assert_called_once()
    call_kwargs = ctx.send.call_args.kwargs
    embed = call_kwargs['embed']
    assert isinstance(embed, discord.Embed)
    assert embed.title == "Monitoring Status"
    
    # Check embed fields
    field_dict = {field.name: field.value for field in embed.fields}
    assert field_dict["Username"] == "test_user"
    assert field_dict["Keyword"] == "test_keyword"
    assert field_dict["Active"] == "Yes"
    assert "Last Checked" in field_dict

@pytest.mark.asyncio
async def test_monitoring_status_no_config(command, mock_db):
    """Test checking monitoring status when no config exists."""
    # Create mock context
    ctx = AsyncMock()
    ctx.send = AsyncMock()
    
    # Configure mock database to return no config
    mock_db.get_monitoring_config.return_value = None
    
    # Test the command
    await command.monitoring_status(command, ctx)
    
    # Verify database call
    mock_db.get_monitoring_config.assert_called_once()
    
    # Verify error message
    ctx.send.assert_called_once()
    error_msg = ctx.send.call_args[0][0]
    assert "No active monitoring configuration" in error_msg

@pytest.mark.asyncio
async def test_check_for_new_posts(command, mock_db):
    """Test the background task for checking new posts."""
    # Mock the sleep function to avoid infinite loop
    with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
        # Configure mock sleep to raise exception after first iteration
        mock_sleep.side_effect = [None, Exception("Stop loop")]
        
        # Configure mock database
        mock_db.is_monitoring_active.return_value = True
        mock_config = {
            'username': 'test_user',
            'filter_keyword': 'test_keyword',
            'last_post_id': None
        }
        mock_db.get_monitoring_config.return_value = mock_config
        
        # Mock the Truth Social client
        mock_post = MagicMock()
        mock_post.content = "Test post with test_keyword"
        mock_post.id = "123"
        mock_post.user = MagicMock()
        mock_post.user.display_name = "Test Author"
        mock_post.created_at = datetime.now(timezone.utc)
        mock_post.likes_count = 10
        mock_post.replies_count = 5
        mock_post.reposts_count = 3
        
        command.client = MagicMock()
        command.client.get_user_posts = AsyncMock()
        command.client.get_user_posts.return_value.posts = [mock_post]
        
        # Mock bot channels
        mock_channel = AsyncMock(spec=discord.TextChannel)  # Specify it's a TextChannel
        command.bot.get_all_channels.return_value = [mock_channel]
        
        try:
            # Run the background task
            await command._check_for_new_posts()
        except Exception as e:
            assert str(e) == "Stop loop"
        
        # Verify database calls
        mock_db.is_monitoring_active.assert_called()
        mock_db.get_monitoring_config.assert_called()
        
        # Verify post was sent to channel
        mock_channel.send.assert_called()
        call_kwargs = mock_channel.send.call_args.kwargs
        embed = call_kwargs['embed']
        assert isinstance(embed, discord.Embed)
        assert embed.title == "New post by Test Author"
        assert "test_keyword" in embed.description 
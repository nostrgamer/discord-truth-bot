"""Tests for error handling edge cases."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import discord
import aiohttp
from datetime import datetime, timezone
from discord_bot.commands.truth_posts import TruthPostsCommand
from discord_bot.commands.filter_posts import FilterPostsCommand

class MockContext:
    """Simple mock for Discord context."""
    
    def __init__(self):
        self.send_calls = []
        self.author = MagicMock()
        self.author.id = 12345
        self.author.name = "test_user"
        self._typing_cm = AsyncMock()
        self._typing_cm.__aenter__ = AsyncMock()
        self._typing_cm.__aexit__ = AsyncMock(return_value=False)  # Don't suppress exceptions
    
    async def send(self, content=None, embed=None, **kwargs):
        self.send_calls.append((content, embed, kwargs))
        return MagicMock()
    
    def typing(self):
        return self._typing_cm

@pytest.fixture
def truth_posts_command():
    """Create a TruthPostsCommand instance with mocked dependencies."""
    cmd = TruthPostsCommand(MagicMock())
    # Access the command methods directly from the class
    cmd.truth_posts = cmd.truth_posts.callback
    # Initialize the client
    cmd.client = MagicMock()
    return cmd

@pytest.fixture
def filter_posts_command():
    """Create a FilterPostsCommand instance with mocked dependencies."""
    cmd = FilterPostsCommand(MagicMock())
    # Access the command methods directly from the class
    cmd.filter_posts = cmd.filter_posts.callback
    # Initialize the client
    cmd.client = MagicMock()
    return cmd

@pytest.mark.asyncio
async def test_network_timeout():
    """Test behavior when API requests time out."""
    # Create command and context
    cmd = TruthPostsCommand(MagicMock())
    ctx = MockContext()
    
    # Configure client to simulate timeout
    cmd.client = MagicMock()
    cmd.client.get_user_posts = AsyncMock(side_effect=aiohttp.ClientConnectionError("Connection timeout"))
    
    # Patching the typing CM to ensure exception is propagated to our try/except
    ctx._typing_cm.__aenter__.return_value = None
    ctx._typing_cm.__aexit__.return_value = False  # Don't suppress exceptions
    
    # Test the command directly using the callback method
    await cmd.truth_posts.callback(cmd, ctx, "username")
    
    # Verify error message was sent with the exact expected format
    assert any("Error fetching posts: Connection timeout" in msg for msg, _, _ in ctx.send_calls), \
        f"Error message not found. Messages: {[msg for msg, _, _ in ctx.send_calls]}"

@pytest.mark.asyncio
async def test_api_rate_limit():
    """Test behavior when hitting API rate limits."""
    # Create command and context
    cmd = FilterPostsCommand(MagicMock())
    ctx = MockContext()
    
    # Ensure cooldown is disabled
    with patch.object(cmd, '_is_on_cooldown', return_value=False):
        # Add our custom exception
        rate_limit_error = Exception("Rate limit exceeded")
        
        # Setup context manager behavior to ensure exception propagation
        ctx._typing_cm.__aenter__.return_value = None
        ctx._typing_cm.__aexit__.return_value = False
        
        # Setup client to raise exception during get_user_posts
        cmd.client = MagicMock()
        cmd.client.get_user_posts = AsyncMock(side_effect=rate_limit_error)
        
        # Test the command
        await cmd.filter_posts.callback(cmd, ctx, "username")
        
        # Check for the specific error message format
        assert any("Error filtering posts: Rate limit exceeded" in msg for msg, _, _ in ctx.send_calls), \
            f"Rate limit error message not found. Messages: {[msg for msg, _, _ in ctx.send_calls]}"

@pytest.mark.asyncio
async def test_empty_username():
    """Test behavior with empty username."""
    # Create command and context
    cmd = TruthPostsCommand(MagicMock())
    ctx = MockContext()
    
    # Configure client first, before calling the command
    cmd.client = MagicMock()
    cmd.client.get_user_posts = AsyncMock(return_value=MagicMock(posts=[]))
    
    # Test the command with empty username
    await cmd.truth_posts.callback(cmd, ctx, "")
    
    # Verify client was called with empty string
    cmd.client.get_user_posts.assert_called_once()
    called_args = cmd.client.get_user_posts.call_args
    assert called_args[0][0] == "", "Empty username not passed correctly"

@pytest.mark.asyncio
async def test_malformed_api_response():
    """Test behavior when API returns malformed data."""
    # Create command and context
    cmd = FilterPostsCommand(MagicMock())
    ctx = MockContext()
    
    # Ensure cooldown is disabled
    with patch.object(cmd, '_is_on_cooldown', return_value=False):
        # Configure typing and context manager for proper exception handling
        ctx._typing_cm.__aenter__.return_value = None
        ctx._typing_cm.__aexit__.return_value = False
        
        # Configure client to return malformed data that will trigger AttributeError
        cmd.client = MagicMock()
        # This will cause AttributeError when code tries to access posts.posts
        mock_bad_response = object()  # Object with no 'posts' attribute
        cmd.client.get_user_posts = AsyncMock(return_value=mock_bad_response)
        
        # Test the command
        await cmd.filter_posts.callback(cmd, ctx, "username")
        
        # Check for error message about AttributeError - exact format will depend on the code
        assert len(ctx.send_calls) > 0, f"No messages sent at all"
        
        # Look for error messages related to not having a 'posts' attribute
        error_messages = [msg for msg, _, _ in ctx.send_calls if msg and "Error" in msg]
        assert error_messages, f"No error message found. Messages: {[msg for msg, _, _ in ctx.send_calls]}"
        assert "AttributeError" in error_messages[0] or "'posts'" in error_messages[0], \
            f"Expected error about missing 'posts' attribute, got: {error_messages[0]}"

@pytest.mark.asyncio
async def test_excessive_cooldown_spam():
    """Test behavior when command is spammed and hits cooldown."""
    # Create command and context
    cmd = FilterPostsCommand(MagicMock())
    ctx = MockContext()
    
    # Force cooldown to be active
    with patch.object(cmd, '_is_on_cooldown', return_value=True):
        cmd._cooldown_time = 30
        cmd._cooldowns[ctx.author.id] = [datetime.now()]
        
        # Call command multiple times in quick succession
        await cmd.filter_posts.callback(cmd, ctx, "username")
        await cmd.filter_posts.callback(cmd, ctx, "username")
        await cmd.filter_posts.callback(cmd, ctx, "username")
    
    # Verify cooldown messages were sent each time
    cooldown_messages = [msg for msg, _, _ in ctx.send_calls if msg and "wait" in msg.lower()]
    assert len(cooldown_messages) == 3, "Not all spam attempts were properly rate-limited"

@pytest.mark.asyncio
async def test_very_long_username():
    """Test behavior with extremely long username."""
    # Create command and context
    cmd = TruthPostsCommand(MagicMock())
    ctx = MockContext()
    
    # Configure client
    cmd.client = MagicMock()
    cmd.client.get_user_posts = AsyncMock(return_value=MagicMock(posts=[]))
    
    # Create an excessively long username
    long_username = "a" * 1000
    
    # Test the command with long username
    await cmd.truth_posts.callback(cmd, ctx, long_username)
    
    # Verify the command processed the long username without crashing
    cmd.client.get_user_posts.assert_called_once()
    called_args = cmd.client.get_user_posts.call_args[0]
    assert called_args[0] == long_username, "Long username was not passed correctly"

@pytest.mark.asyncio
async def test_unicode_characters_in_username():
    """Test behavior with unicode characters in username."""
    # Create command and context
    cmd = TruthPostsCommand(MagicMock())
    ctx = MockContext()
    
    # Configure client
    cmd.client = MagicMock()
    cmd.client.get_user_posts = AsyncMock(return_value=MagicMock(posts=[]))
    
    # Create a username with various Unicode characters
    unicode_username = "🔥😊é科技ñüåß"
    
    # Test the command with unicode username
    await cmd.truth_posts.callback(cmd, ctx, unicode_username)
    
    # Verify the command processed the unicode username without crashing
    cmd.client.get_user_posts.assert_called_once()
    called_args = cmd.client.get_user_posts.call_args[0]
    assert called_args[0] == unicode_username, "Unicode username not passed correctly" 
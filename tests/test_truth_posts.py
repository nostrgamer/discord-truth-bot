"""Tests for the truth_posts command."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import discord
from datetime import datetime, timezone
from discord_bot.commands.truth_posts import TruthPostsCommand

class AsyncContextManagerMock:
    """Mock for async context managers."""
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

@pytest.fixture
def mock_bot():
    """Create a mock bot instance."""
    bot = MagicMock()
    return bot

@pytest.fixture
def command(mock_bot):
    """Create a TruthPostsCommand instance with mocked dependencies."""
    cmd = TruthPostsCommand(mock_bot)
    # Access the command methods directly from the class
    cmd.truth_posts = cmd.truth_posts.callback
    # Initialize the client
    cmd.client = MagicMock()
    return cmd

@pytest.mark.asyncio
async def test_truth_posts_success(command):
    """Test successful fetching and display of Truth Social posts."""
    # Create mock context
    ctx = AsyncMock()
    ctx.send = AsyncMock()
    ctx.typing = MagicMock(return_value=AsyncContextManagerMock())
    ctx.author.name = "test_user"
    
    # Create mock posts
    mock_post = MagicMock()
    mock_post.user = MagicMock()
    mock_post.user.display_name = "Test Author"
    mock_post.user.username = "testauthor"
    mock_post.id = "123"
    mock_post.content = "Test post content"
    mock_post.created_at = datetime.now(timezone.utc)
    mock_post.likes_count = 100
    mock_post.replies_count = 50
    mock_post.reposts_count = 25
    
    mock_posts = MagicMock()
    mock_posts.posts = [mock_post]
    
    # Configure the client mock
    command.client.get_user_posts = AsyncMock(return_value=mock_posts)
    
    # Test the command
    await command.truth_posts(command, ctx, "testauthor")
    
    # Verify client call
    command.client.get_user_posts.assert_called_once_with("testauthor", limit=5)
    
    # Verify typing context was used
    ctx.typing.assert_called_once()
    
    # Verify embed was sent
    ctx.send.assert_called_once()
    call_kwargs = ctx.send.call_args.kwargs
    embed = call_kwargs['embed']
    
    # Verify embed contents
    assert isinstance(embed, discord.Embed)
    assert embed.title == "Post 1 by Test Author"
    assert embed.description == "Test post content"
    assert embed.url == "https://truthsocial.com/@testauthor/123"
    assert embed.color == discord.Color.blue()
    
    # Verify embed fields
    field_dict = {field.name: field.value for field in embed.fields}
    assert field_dict["Likes"] == "100"
    assert field_dict["Replies"] == "50"
    assert field_dict["Reposts"] == "25"
    
    # Verify footer
    assert embed.footer.text == "Requested by test_user"

@pytest.mark.asyncio
async def test_truth_posts_with_at_symbol(command):
    """Test that @ symbol is properly stripped from username."""
    # Create mock context
    ctx = AsyncMock()
    ctx.send = AsyncMock()
    ctx.typing = MagicMock(return_value=AsyncContextManagerMock())
    
    # Configure the client mock
    command.client.get_user_posts = AsyncMock(return_value=MagicMock(posts=[]))
    
    # Test the command with @ symbol
    await command.truth_posts(command, ctx, "@testauthor")
    
    # Verify client call without @ symbol
    command.client.get_user_posts.assert_called_once_with("testauthor", limit=5)

@pytest.mark.asyncio
async def test_truth_posts_no_posts(command):
    """Test handling of users with no posts."""
    # Create mock context
    ctx = AsyncMock()
    ctx.send = AsyncMock()
    ctx.typing = MagicMock(return_value=AsyncContextManagerMock())
    
    # Configure the client mock
    command.client.get_user_posts = AsyncMock(return_value=MagicMock(posts=[]))
    
    # Test the command
    await command.truth_posts(command, ctx, "testauthor")
    
    # Verify client call
    command.client.get_user_posts.assert_called_once_with("testauthor", limit=5)
    
    # Verify no embeds were sent (since there were no posts)
    assert not ctx.send.called

@pytest.mark.asyncio
async def test_truth_posts_error(command):
    """Test error handling when fetching posts fails."""
    # Create mock context
    ctx = AsyncMock()
    ctx.send = AsyncMock()
    ctx.typing = MagicMock(return_value=AsyncContextManagerMock())
    
    # Configure the client mock to raise an exception
    command.client.get_user_posts = AsyncMock(side_effect=Exception("Test error"))
    
    # Test the command
    await command.truth_posts(command, ctx, "testauthor")
    
    # Verify error message was sent
    ctx.send.assert_called_once_with("Error fetching posts: Test error") 
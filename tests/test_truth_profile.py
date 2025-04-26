"""Tests for the truth_profile command."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import discord
from datetime import datetime, timezone
from discord_bot.commands.truth_profile import TruthProfileCommand

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
    """Create a TruthProfileCommand instance with mocked dependencies."""
    cmd = TruthProfileCommand(mock_bot)
    # Access the command methods directly from the class
    cmd.truth_profile = cmd.truth_profile.callback
    # Initialize the client
    cmd.client = MagicMock()
    return cmd

@pytest.mark.asyncio
async def test_truth_profile_success(command):
    """Test successful fetching and display of Truth Social profile."""
    # Create mock context
    ctx = AsyncMock()
    ctx.send = AsyncMock()
    ctx.typing = MagicMock(return_value=AsyncContextManagerMock())
    ctx.author.name = "test_user"
    
    # Create mock profile
    mock_profile = MagicMock()
    mock_profile.display_name = "Test User"
    mock_profile.username = "testuser"
    mock_profile.is_verified = True
    mock_profile.followers_count = 1000
    mock_profile.following_count = 500
    mock_profile.posts_count = 100
    mock_profile.created_at = datetime.now(timezone.utc)
    mock_profile.bio = "Test user bio"
    
    # Configure the client mock
    command.client.get_user_profile = AsyncMock(return_value=mock_profile)
    
    # Test the command
    await command.truth_profile(command, ctx, "testuser")
    
    # Verify client call
    command.client.get_user_profile.assert_called_once_with("testuser")
    
    # Verify typing context was used
    ctx.typing.assert_called_once()
    
    # Verify embed was sent
    ctx.send.assert_called_once()
    call_kwargs = ctx.send.call_args.kwargs
    embed = call_kwargs['embed']
    
    # Verify embed contents
    assert isinstance(embed, discord.Embed)
    assert embed.title == f"Truth Social Profile: {mock_profile.display_name}"
    assert embed.url == f"https://truthsocial.com/@{mock_profile.username}"
    assert embed.color == discord.Color.blue()
    
    # Verify embed fields
    field_dict = {field.name: field.value for field in embed.fields}
    assert field_dict["Username"] == f"@{mock_profile.username}"
    assert field_dict["Verified"] == "✅"
    assert field_dict["Followers"] == "1,000"
    assert field_dict["Following"] == "500"
    assert field_dict["Posts"] == "100"
    assert field_dict["Bio"] == "Test user bio"
    
    # Verify footer
    assert embed.footer.text == "Requested by test_user"

@pytest.mark.asyncio
async def test_truth_profile_with_at_symbol(command):
    """Test that @ symbol is properly stripped from username."""
    # Create mock context
    ctx = AsyncMock()
    ctx.send = AsyncMock()
    ctx.typing = MagicMock(return_value=AsyncContextManagerMock())
    
    # Configure the client mock
    command.client.get_user_profile = AsyncMock(return_value=MagicMock())
    
    # Test the command with @ symbol
    await command.truth_profile(command, ctx, "@testuser")
    
    # Verify client call without @ symbol
    command.client.get_user_profile.assert_called_once_with("testuser")

@pytest.mark.asyncio
async def test_truth_profile_no_bio(command):
    """Test profile display when bio is not available."""
    # Create mock context
    ctx = AsyncMock()
    ctx.send = AsyncMock()
    ctx.typing = MagicMock(return_value=AsyncContextManagerMock())
    ctx.author.name = "test_user"
    
    # Create mock profile without bio
    mock_profile = MagicMock()
    mock_profile.display_name = "Test User"
    mock_profile.username = "testuser"
    mock_profile.is_verified = False
    mock_profile.followers_count = 1000
    mock_profile.following_count = 500
    mock_profile.posts_count = 100
    mock_profile.created_at = datetime.now(timezone.utc)
    mock_profile.bio = None
    
    # Configure the client mock
    command.client.get_user_profile = AsyncMock(return_value=mock_profile)
    
    # Test the command
    await command.truth_profile(command, ctx, "testuser")
    
    # Verify embed was sent
    ctx.send.assert_called_once()
    call_kwargs = ctx.send.call_args.kwargs
    embed = call_kwargs['embed']
    
    # Verify bio field is not present
    field_dict = {field.name: field.value for field in embed.fields}
    assert "Bio" not in field_dict
    
    # Verify verification status shows as ❌
    assert field_dict["Verified"] == "❌"

@pytest.mark.asyncio
async def test_truth_profile_error(command):
    """Test error handling when fetching profile fails."""
    # Create mock context
    ctx = AsyncMock()
    ctx.send = AsyncMock()
    ctx.typing = MagicMock(return_value=AsyncContextManagerMock())
    
    # Configure the client mock to raise an exception
    command.client.get_user_profile = AsyncMock(side_effect=Exception("Test error"))
    
    # Test the command
    await command.truth_profile(command, ctx, "testuser")
    
    # Verify error message was sent
    ctx.send.assert_called_once_with("Error fetching profile: Test error") 
"""Common test fixtures for Discord Truth Social Bot tests."""

import pytest
from discord import Message, User, TextChannel, Guild, Member, Embed
from unittest.mock import AsyncMock, MagicMock, patch
import os
from types import SimpleNamespace

class AsyncContextManager:
    """A context manager that can be used in async with statements."""
    def __init__(self):
        self.entered = False
        self.exited = False

    async def __aenter__(self):
        self.entered = True
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.exited = True
        return None

@pytest.fixture(autouse=True)
def mock_env():
    """Mock environment variables."""
    with patch.dict(os.environ, {
        'APIFY_API_TOKEN': 'test_token',
        'APIFY_ACTOR_ID': 'test_actor'
    }):
        yield

@pytest.fixture
def mock_message():
    """Create a mock Discord message/context."""
    message = AsyncMock()
    message.author = MagicMock(spec=Member)
    message.author.name = "test_user"
    message.channel = AsyncMock(spec=TextChannel)
    message.guild = MagicMock(spec=Guild)
    message.content = ""
    
    # Add context-like attributes
    message.send = AsyncMock()
    
    # Create a proper async context manager for typing
    async def mock_typing():
        cm = AsyncContextManager()
        return cm
    
    message.typing = AsyncMock(side_effect=mock_typing)
    
    # Add command context attributes
    message.bot = None  # Will be set by the fixture that uses it
    message.command = None  # Will be set by the command being tested
    message.invoked_with = "profile"
    message.prefix = "!"
    
    # Configure send mock to handle embeds properly
    async def mock_send(*args, **kwargs):
        # Handle both positional and keyword arguments for embed
        embed = kwargs.get('embed') or (args[0] if args and isinstance(args[0], Embed) else None)
        return SimpleNamespace(id='123456789')
    
    message.send.side_effect = mock_send
    message.channel.send.side_effect = mock_send
    
    return message

@pytest.fixture
def mock_bot():
    """Create a mock Discord bot."""
    bot = AsyncMock()
    bot.user = MagicMock(spec=User)
    return bot

@pytest.fixture(autouse=True)
def mock_truth_social_client():
    """Mock TruthSocialClient and its methods."""
    with patch('truth_social.client.TruthSocialClient') as mock_client:
        client_instance = AsyncMock()
        client_instance.get_user_profile = AsyncMock()
        client_instance.get_user_posts = AsyncMock()
        mock_client.return_value = client_instance
        yield client_instance 
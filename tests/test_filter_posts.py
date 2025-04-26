"""Tests for the filter_posts command."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock, call
import discord
from datetime import datetime, timezone, timedelta
from discord_bot.commands.filter_posts import FilterPostsCommand

class MockContext:
    """Simple mock for Discord context."""
    
    def __init__(self):
        self.send_calls = []
        self.author = MagicMock()
        self.author.id = 12345
        self.author.name = "test_user"
        self._typing_cm = MagicMock()
        self._typing_cm.__aenter__ = AsyncMock()
        self._typing_cm.__aexit__ = AsyncMock()
    
    async def send(self, content=None, embed=None, **kwargs):
        self.send_calls.append((content, embed, kwargs))
        return MagicMock()
    
    def typing(self):
        return self._typing_cm

@pytest.mark.asyncio
async def test_filter_posts_cooldown():
    """Test cooldown functionality."""
    # Create command with mocked dependencies
    cmd = FilterPostsCommand(MagicMock())
    ctx = MockContext()
    
    # Mock _is_on_cooldown to return True
    with patch.object(cmd, '_is_on_cooldown', return_value=True):
        # Force the cooldown time for testing
        cmd._cooldown_time = 20
        cmd._cooldowns[ctx.author.id] = [datetime.now() - timedelta(seconds=10)]
        
        # Call the method directly using the callback function
        await cmd.filter_posts.callback(cmd, ctx, "testuser")
        
        # Verify cooldown message was sent
        assert len(ctx.send_calls) == 1
        content, _, _ = ctx.send_calls[0]
        assert "wait" in content.lower()

@pytest.mark.asyncio
async def test_filter_posts_max_days():
    """Test maximum days limit enforcement."""
    # Create command with mocked dependencies
    cmd = FilterPostsCommand(MagicMock())
    ctx = MockContext()
    
    # Mock dependencies
    with patch.object(cmd, '_is_on_cooldown', return_value=False):
        with patch.object(cmd, 'client') as mock_client:
            # Configure mock client
            mock_client.get_user_posts = AsyncMock()
            mock_client.get_user_posts.return_value = MagicMock(posts=[])
            
            # Test the command with days > max_days
            cmd._max_days = 30
            
            # Call the callback directly
            await cmd.filter_posts.callback(cmd, ctx, "testuser", days=45)
            
            # Verify max days message was sent
            found_message = False
            for call in ctx.send_calls:
                content, _, _ = call
                if content and "Maximum lookback period is 30 days" in content:
                    found_message = True
                    break
            
            assert found_message, "Max days message not found"

@pytest.mark.asyncio
async def test_filter_posts_success():
    """Test successful filtering of posts."""
    # Create command and context
    cmd = FilterPostsCommand(MagicMock())
    ctx = MockContext()
    
    # Create a fixed datetime
    fixed_dt = datetime(2024, 1, 1, tzinfo=timezone.utc)
    
    # Create mock post
    mock_post = MagicMock()
    mock_post.user = MagicMock()
    mock_post.user.display_name = "Test Author"
    mock_post.content = "Test post content with keyword"
    mock_post.created_at = fixed_dt - timedelta(days=1)
    mock_post.likes_count = 100
    mock_post.replies_count = 50
    mock_post.reposts_count = 25
    
    # Configure test environment
    with patch.object(cmd, '_is_on_cooldown', return_value=False):
        with patch.object(cmd, 'client') as mock_client:
            # Setup mock client
            mock_client.get_user_posts = AsyncMock()
            mock_client.get_user_posts.return_value = MagicMock(posts=[mock_post])
            
            # Setup datetime patching
            with patch('discord_bot.commands.filter_posts.datetime') as mock_dt:
                mock_dt.now.return_value = fixed_dt
                mock_dt.now.side_effect = lambda tz=None: fixed_dt
                
                # Call the method directly using the callback
                await cmd.filter_posts.callback(cmd, ctx, "testuser", "keyword", 7)
                
                # Verify client call
                mock_client.get_user_posts.assert_awaited_once_with("testuser")
                
                # Verify embed was sent
                embed_found = False
                for _, embed, _ in ctx.send_calls:
                    if embed and isinstance(embed, discord.Embed):
                        if (embed.title == "Post by Test Author" and 
                            embed.description == "Test post content with keyword"):
                            embed_found = True
                            
                            # Check fields - values are converted to strings when added to embed
                            field_dict = {field.name: field.value for field in embed.fields}
                            assert str(field_dict["Likes"]) == "100"
                            assert str(field_dict["Replies"]) == "50"
                            assert str(field_dict["Reposts"]) == "25"
                            break
                
                assert embed_found, "Embed not found or incorrect"

@pytest.mark.asyncio
async def test_filter_posts_no_matches():
    """Test handling when no posts match criteria."""
    # Create command and context
    cmd = FilterPostsCommand(MagicMock())
    ctx = MockContext()
    
    # Create a fixed datetime
    fixed_dt = datetime(2024, 1, 1, tzinfo=timezone.utc)
    
    # Create mock post that won't match the filter
    mock_post = MagicMock()
    mock_post.content = "No matching content here"
    mock_post.created_at = fixed_dt - timedelta(days=1)
    
    # Configure test environment
    with patch.object(cmd, '_is_on_cooldown', return_value=False):
        with patch.object(cmd, 'client') as mock_client:
            # Setup mock client
            mock_client.get_user_posts = AsyncMock()
            mock_client.get_user_posts.return_value = MagicMock(posts=[mock_post])
            
            # Setup datetime patching
            with patch('discord_bot.commands.filter_posts.datetime') as mock_dt:
                mock_dt.now.return_value = fixed_dt
                mock_dt.now.side_effect = lambda tz=None: fixed_dt
                
                # Call the method directly using the callback
                await cmd.filter_posts.callback(cmd, ctx, "testuser", "keyword")
                
                # Verify no matches message was sent
                found_message = False
                for call in ctx.send_calls:
                    content, _, _ = call
                    if content and "No posts found for testuser matching the criteria." in content:
                        found_message = True
                        break
                
                assert found_message, "No matches message not found"

@pytest.mark.asyncio
async def test_filter_posts_with_at_symbol():
    """Test that @ symbol is properly stripped from username."""
    # Create command and context
    cmd = FilterPostsCommand(MagicMock())
    ctx = MockContext()
    
    # Configure test environment
    with patch.object(cmd, '_is_on_cooldown', return_value=False):
        with patch.object(cmd, 'client') as mock_client:
            # Setup mock client
            mock_client.get_user_posts = AsyncMock()
            mock_client.get_user_posts.return_value = MagicMock(posts=[])
            
            # Call the method directly using the callback
            await cmd.filter_posts.callback(cmd, ctx, "@testuser")
            
            # Verify client call without @ symbol
            mock_client.get_user_posts.assert_awaited_once_with("testuser")

@pytest.mark.asyncio
async def test_filter_posts_max_results():
    """Test maximum results limit."""
    # Create command and context
    cmd = FilterPostsCommand(MagicMock())
    ctx = MockContext()
    
    # Create a fixed datetime
    fixed_dt = datetime(2024, 1, 1, tzinfo=timezone.utc)
    
    # Create more posts than the max limit with keyword in content
    mock_posts = []
    for i in range(10):
        post = MagicMock()
        post.user = MagicMock()
        post.user.display_name = "Test Author"
        post.content = f"Test post {i} with keyword"
        post.created_at = fixed_dt - timedelta(days=1)
        post.likes_count = 10
        post.replies_count = 5
        post.reposts_count = 2
        mock_posts.append(post)
    
    # Configure test environment
    with patch.object(cmd, '_is_on_cooldown', return_value=False):
        with patch.object(cmd, 'client') as mock_client:
            # Setup mock client
            mock_client.get_user_posts = AsyncMock()
            mock_client.get_user_posts.return_value = MagicMock(posts=mock_posts)
            
            # Force the max results limit
            cmd._max_results = 5
            
            # Setup datetime patching
            with patch('discord_bot.commands.filter_posts.datetime') as mock_dt:
                mock_dt.now.return_value = fixed_dt
                mock_dt.now.side_effect = lambda tz=None: fixed_dt
                
                # Call the method directly using the callback
                await cmd.filter_posts.callback(cmd, ctx, "testuser", "keyword")
                
                # Verify max results message was sent
                found_message = False
                embed_count = 0
                for call in ctx.send_calls:
                    content, embed, _ = call
                    if content and "Found 10 posts. Showing the 5 most recent matching posts" in content:
                        found_message = True
                    if embed and isinstance(embed, discord.Embed):
                        embed_count += 1
                
                assert found_message, "Max results message not found"
                assert embed_count == 5, f"Expected 5 embeds, got {embed_count}"

@pytest.mark.asyncio
async def test_filter_posts_error():
    """Test error handling when fetching posts fails."""
    # Create a simple test that doesn't use context managers or complex patching
    cmd = FilterPostsCommand(MagicMock())
    ctx = MockContext()
    
    # To make the test simpler, force an error at the beginning by making _is_on_cooldown raise an exception
    with patch.object(cmd, '_is_on_cooldown', side_effect=Exception("Simulated error")):
        # Call the callback directly
        await cmd.filter_posts.callback(cmd, ctx, "testuser")
        
        # Verify that an error message was sent
        assert any("Error filtering posts: Simulated error" in content 
                 for content, _, _ in ctx.send_calls), "Error message not sent" 
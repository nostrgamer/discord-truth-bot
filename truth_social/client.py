from apify_client import ApifyClient
from typing import Optional, Dict, Any, List
from datetime import datetime
from .config import ApifyConfig
from .models import UserProfile, Post, PostList

class ApifyError(Exception):
    """Base exception for Apify API errors."""
    pass

class TruthSocialClient:
    """Client for interacting with Truth Social via Apify."""
    
    def __init__(self, config: ApifyConfig):
        self.config = config
        self._client = ApifyClient(config.api_token)
        
    async def _run_actor(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the Apify actor and wait for results."""
        # Map input to Truth Social Scraper schema
        default_input = {
            "identifiers": [],
            "fetchPosts": True,
            "cleanContent": True,
            "onlyMedia": False,
            "onlyReplies": False,
            "useLastPostId": False,
            "maxPosts": 20  # Default to 20 posts
        }
        
        # Map our input to the actor's expected format
        if "username" in input_data:
            default_input["identifiers"] = [input_data.pop("username")]
        if "maxPosts" in input_data:
            # Ensure maxPosts is at least 5
            default_input["maxPosts"] = max(5, input_data.pop("maxPosts"))
            
        # Merge with any remaining input data
        input_data = {**default_input, **input_data}
        
        try:
            # Run the actor
            run = self._client.actor(self.config.actor_id).call(run_input=input_data)
            
            # Get the dataset items
            dataset = self._client.dataset(run["defaultDatasetId"])
            return list(dataset.iterate_items())
            
        except Exception as e:
            raise ApifyError(f"Failed to run actor: {str(e)}")
            
    async def get_user_profile(self, username: str) -> UserProfile:
        """Get user profile information."""
        results = await self._run_actor({
            "username": username,
            "maxPosts": 0,  # We only want profile data
            "fetchPosts": False  # Don't fetch posts for profile
        })
        
        if not results:
            raise ApifyError(f"No profile found for username: {username}")
            
        profile_data = results[0]['account']
        return UserProfile(
            username=profile_data['username'],
            display_name=profile_data['display_name'],
            bio=profile_data.get('note', '').replace('<p>', '').replace('</p>', ''),
            followers_count=profile_data['followers_count'],
            following_count=profile_data['following_count'],
            posts_count=profile_data['statuses_count'],
            created_at=datetime.fromisoformat(profile_data['created_at']),
            is_verified=profile_data['verified']
        )
            
    async def get_user_posts(self, username: str, limit: int = 20) -> PostList:
        """Get user's recent posts."""
        results = await self._run_actor({
            "username": username,
            "maxPosts": limit,
            "fetchPosts": True
        })
        
        if not results:
            raise ApifyError(f"No posts found for username: {username}")
            
        # Get the profile data from the first result
        profile_data = results[0]['account']
        author = UserProfile(
            username=profile_data['username'],
            display_name=profile_data['display_name'],
            bio=profile_data.get('note', '').replace('<p>', '').replace('</p>', ''),
            followers_count=profile_data['followers_count'],
            following_count=profile_data['following_count'],
            posts_count=profile_data['statuses_count'],
            created_at=datetime.fromisoformat(profile_data['created_at']),
            is_verified=profile_data['verified']
        )
            
        posts = []
        for post_data in results:
            post = Post(
                id=post_data['id'],
                content=post_data['content'],
                author=author,  # Use the same author profile for all posts
                created_at=datetime.fromisoformat(post_data['created_at']),
                likes_count=post_data['favourites_count'],
                replies_count=post_data['replies_count'],
                reposts_count=post_data['reblogs_count'],
                is_repost=post_data['reblog'] is not None,
                original_post=None  # We'll handle this if needed
            )
            posts.append(post)
            
        return PostList(
            posts=posts,
            next_cursor=None,  # Apify doesn't use cursors
            previous_cursor=None
        )
            
    async def get_post(self, post_id: str) -> Post:
        """Get a specific post by ID."""
        # Since Apify doesn't support direct post fetching,
        # we'll need to get the user's posts and find the specific one
        # This is a limitation of the current Apify actor
        raise NotImplementedError("Direct post fetching is not supported by the current Apify actor")
            
    async def search_users(self, query: str, limit: int = 20) -> List[UserProfile]:
        """Search for users by username or display name."""
        # Since Apify doesn't support user search,
        # we'll need to implement this differently
        raise NotImplementedError("User search is not supported by the current Apify actor") 
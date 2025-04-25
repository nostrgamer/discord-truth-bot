from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class UserProfile:
    """Represents a Truth Social user profile."""
    username: str
    display_name: str
    bio: Optional[str]
    followers_count: int
    following_count: int
    posts_count: int
    created_at: datetime
    is_verified: bool
    
@dataclass
class Post:
    """Represents a Truth Social post."""
    id: str
    content: str
    author: UserProfile
    created_at: datetime
    likes_count: int
    replies_count: int
    reposts_count: int
    is_repost: bool
    original_post: Optional['Post'] = None
    
@dataclass
class PostList:
    """Represents a list of posts with pagination info."""
    posts: List[Post]
    next_cursor: Optional[str]
    previous_cursor: Optional[str] 
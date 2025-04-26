from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Union

@dataclass
class User:
    """Represents a Truth Social user."""
    id: str
    username: str
    display_name: str
    description: Optional[str] = None
    followers_count: int = 0
    following_count: int = 0
    posts_count: int = 0
    avatar_url: Optional[str] = None
    total_likes: Optional[int] = None
    total_replies: Optional[int] = None

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
    location: Optional[str] = None
    avatar_url: Optional[str] = None
    
@dataclass
class Post:
    """Represents a Truth Social post."""
    id: str
    content: str
    created_at: datetime
    likes_count: int
    replies_count: int
    reposts_count: int
    is_repost: bool = False
    user: Optional[Union[User, UserProfile]] = None
    original_post: Optional['Post'] = None
    
@dataclass
class PostList:
    """Represents a list of posts with pagination info."""
    posts: List[Post]
    next_cursor: Optional[str] = None
    previous_cursor: Optional[str] = None 
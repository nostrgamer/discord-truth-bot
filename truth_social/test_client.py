import asyncio
import os
from dotenv import load_dotenv
from truth_social.client import TruthSocialClient
from truth_social.config import ApifyConfig

async def test_client():
    # Load environment variables
    load_dotenv()
    api_token = os.getenv("APIFY_API_TOKEN")
    
    if not api_token:
        print("APIFY_API_TOKEN not found in .env file")
        return
        
    # Initialize the client
    config = ApifyConfig(
        api_token=api_token,
        actor_id="muhammetakkurtt/truth-social-scraper"
    )
    client = TruthSocialClient(config)
    
    try:
        # Test user profile
        print("\nTesting user profile fetch...")
        profile = await client.get_user_profile("@realDonaldTrump")
        print(f"Profile fetched successfully:")
        print(f"Username: {profile.username}")
        print(f"Display Name: {profile.display_name}")
        print(f"Followers: {profile.followers_count}")
        print(f"Following: {profile.following_count}")
        print(f"Posts: {profile.posts_count}")
        print(f"Verified: {profile.is_verified}")
        
        # Test user posts
        print("\nTesting posts fetch...")
        posts = await client.get_user_posts("@realDonaldTrump", limit=5)  # Minimum 5 posts required
        print(f"Fetched {len(posts.posts)} posts:")
        for i, post in enumerate(posts.posts, 1):
            print(f"\nPost {i}:")
            print(f"Content: {post.content[:100]}...")
            print(f"Likes: {post.likes_count}")
            print(f"Replies: {post.replies_count}")
            print(f"Reposts: {post.reposts_count}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_client()) 
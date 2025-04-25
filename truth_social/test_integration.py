import asyncio
from truth_social import ApifyConfig, TruthSocialClient

async def test_integration():
    # Load configuration
    config = ApifyConfig.from_env()
    if not config:
        print("Failed to load configuration. Please check your .env file.")
        print("Make sure you have APIFY_API_TOKEN set in your .env file.")
        return

    try:
        async with TruthSocialClient(config) as client:
            # Test basic user profile fetch
            print("Testing user profile fetch...")
            profile = await client.get_user_profile("realDonaldTrump")  # Using a known account for testing
            print(f"Successfully fetched profile for {profile.username}")
            print(f"Display Name: {profile.display_name}")
            print(f"Followers: {profile.followers_count}")
            
            # Test basic posts fetch
            print("\nTesting posts fetch...")
            posts = await client.get_user_posts("realDonaldTrump", limit=3)
            print(f"Successfully fetched {len(posts.posts)} posts")
            for post in posts.posts:
                print(f"\nPost: {post.content[:100]}...")
                print(f"Likes: {post.likes_count}")
            
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_integration()) 
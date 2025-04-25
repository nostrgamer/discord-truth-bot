from apify_client import ApifyClient
import os
from dotenv import load_dotenv

def test_actor():
    # Load environment variables
    load_dotenv()
    api_token = os.getenv("APIFY_API_TOKEN")
    
    if not api_token:
        print("APIFY_API_TOKEN not found in .env file")
        return
        
    # Initialize the Apify client
    client = ApifyClient(api_token)
    
    try:
        # Prepare the actor input
        run_input = {
            "identifiers": ["@realDonaldTrump"],
            "fetchPosts": True,
            "maxPosts": 20,
            "cleanContent": True,
            "onlyMedia": False,
            "onlyReplies": False,
            "useLastPostId": False
        }
        
        # Run the actor
        print("Starting actor run...")
        run = client.actor("muhammetakkurtt/truth-social-scraper").call(run_input=run_input)
        
        # Get the results
        print("Fetching results...")
        dataset = client.dataset(run["defaultDatasetId"])
        
        # Print the first item
        for item in dataset.iterate_items():
            print("\nFirst item:")
            print(item)
            break
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_actor() 
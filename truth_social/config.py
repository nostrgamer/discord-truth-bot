from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv

@dataclass
class ApifyConfig:
    """Configuration for Apify API integration."""
    api_token: str
    actor_id: str = "muhammetakkurtt/truth-social-scraper"
    base_url: str = "https://api.apify.com/v2/"
    timeout: int = 30

    @classmethod
    def from_env(cls) -> Optional['ApifyConfig']:
        """Create configuration from environment variables."""
        load_dotenv()
        
        api_token = os.getenv("APIFY_API_TOKEN")
        
        if not api_token:
            return None
            
        return cls(
            api_token=api_token
        ) 
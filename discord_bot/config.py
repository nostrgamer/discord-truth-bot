import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass

class BotConfig:
    """Configuration class for the Discord bot."""
    
    def __init__(self):
        # Required configurations
        self.discord_token: str = self._get_required_env('DISCORD_TOKEN')
        
        # Optional configurations with defaults
        self.bot_prefix: str = self._get_optional_env('BOT_PREFIX', '!t')
        
        # Logging configuration
        self.log_level: str = self._get_optional_env('LOG_LEVEL', 'INFO')
        self.log_file: str = self._get_optional_env('LOG_FILE', 'bot.log')
        
        # Validate configurations
        self._validate_config()
        
        # Setup logging
        self._setup_logging()

    def _get_required_env(self, key: str) -> str:
        """Get a required environment variable."""
        value = os.getenv(key)
        if not value:
            raise ConfigError(f"Required environment variable {key} is not set")
        return value

    def _get_optional_env(self, key: str, default: str) -> str:
        """Get an optional environment variable with a default value."""
        return os.getenv(key, default)

    def _validate_config(self) -> None:
        """Validate the configuration values."""
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.log_level not in valid_log_levels:
            raise ConfigError(f"LOG_LEVEL must be one of {valid_log_levels}")

    def _setup_logging(self) -> None:
        """Configure logging based on the settings."""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=getattr(logging, self.log_level),
            format=log_format,
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Logging configured successfully")

# Create a global config instance
try:
    config = BotConfig()
except ConfigError as e:
    logging.error(f"Configuration error: {e}")
    raise 
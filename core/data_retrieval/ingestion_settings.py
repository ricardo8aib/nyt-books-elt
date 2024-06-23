import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    """Configuration settings for the ingestion."""
    # ENVIRONMENT VARIABLES
    API_KEY: str
    END_DATE: str
    START_DATE: str

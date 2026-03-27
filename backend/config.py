from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mock_mode: bool = True
    llm_provider: str = "mock"
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    search_provider: str = "mock"
    tavily_api_key: str = ""
    serper_api_key: str = ""
    canlii_api_key: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

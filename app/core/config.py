from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    database_url:str='postgresql+psycopg://widget:widget@localhost:5433/widgetplatform'
    jwt_secret:str='change-me'
    api_base_url:str='http://localhost:8000'
    widget_version:str='v1'
    cors_allow_origins:str='http://localhost:5500,http://127.0.0.1:5500'
    geo_provider_a_url:str='https://ip-api.com/json/{ip}'
    geo_provider_b_url:str='https://ipapi.co/{ip}/json/'
    class Config: env_file='.env'
settings=Settings()

from pydantic import BaseModel
from template.base.cache_config import CacheConfig
from service.db.database_config import DatabaseConfig

class TemplateConfig(BaseModel):
    """C#의 TemplateConfig 클래스와 동일"""
    app_id: str = ""
    env: str = ""
    local_path: str = ""
    bucket_env: str = ""
    bucket_url: str = ""
    bucket_name: str = ""
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""

class AppConfig(BaseModel):
    template_config: TemplateConfig
    database_config: DatabaseConfig
    cache_config: CacheConfig

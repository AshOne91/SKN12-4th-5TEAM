from typing import List, Optional
from pydantic import BaseModel

class DatabaseTable(BaseModel):
    """C#의 DatabaseTable 클래스와 동일"""
    table_name: str = ""
    pk_name: Optional[str] = None

class DatabaseConfig(BaseModel):
    """C#의 DatabaseConfig 클래스와 동일"""
    database_type: int = 0
    database_name: str = ""
    connection_string: str = ""
    aws_role_arn: str = ""
    aws_role_name: str = ""
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    firestore_product_id: str = ""
    firestore_private_key: str = ""
    tables: List[DatabaseTable] = [] 
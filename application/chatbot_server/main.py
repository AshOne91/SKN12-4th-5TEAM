from fastapi import FastAPI
from contextlib import asynccontextmanager
from application.chatbot_server.routers import account, chatbot, test

from template.base.template_context import TemplateContext
from template.base.template_type import TemplateType
from template.account.account_template_impl import AccountTemplateImpl
from template.chatbot.chatbot_template_impl import ChatbotTemplateImpl

import json
from service.cache.cache_config import CacheConfig
from service.cache.async_session import init_cache
from service.db.database import MySQLPool
from service.http.http_client import HTTPClientPool

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 템플릿 등록
    TemplateContext.add_template(TemplateType.ACCOUNT, AccountTemplateImpl())
    TemplateContext.add_template(TemplateType.CHATBOT, ChatbotTemplateImpl())

    # 캐시(Redis) 초기화
    with open("config.json") as f:
        config = json.load(f)
    cache_config = CacheConfig(**config["cacheConfig"])
    init_cache(cache_config)

    # 글로벌 DB 풀 초기화
    app.state.globaldb = MySQLPool()
    await app.state.globaldb.init(
        host="localhost", port=3306, user="root", password="Wkdwkrdhkd91!", db="medichain_global"
    )

    # pool이 정상적으로 생성됐는지 확인
    if not app.state.globaldb.pool:
        raise RuntimeError("글로벌 DB pool 생성 실패")

    # 샤드 DB 풀 초기화 (글로벌 DB에서 shard_info 읽어서 동적으로 생성)
    app.state.userdb_pools = {}
    async with app.state.globaldb.pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT shard_id, host, port, database_name, username, password FROM shard_info WHERE is_active=1")
            rows = await cur.fetchall()
            for row in rows:
                shard_id, host, port, db_name, username, password = row
                pool = MySQLPool()
                await pool.init(
                    host=host, port=port, user=username, password=password, db=db_name
                )
                app.state.userdb_pools[shard_id] = pool

    # HTTPClientPool 초기화
    app.state.http_client = HTTPClientPool()
    
    # 카테고리 서버 URL 설정
    app.state.category_server_url = config.get("categoryServerUrl", "http://localhost:8001")
    
    yield
    # (필요시 종료 코드)

app = FastAPI(lifespan=lifespan)

app.include_router(test.router, prefix="/test", tags=["test"])
app.include_router(account.router, prefix="/account", tags=["account"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])

@app.get("/")
def root():
    return {"message": "Chatbot Server is running"} 
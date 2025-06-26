from fastapi import FastAPI
from contextlib import asynccontextmanager
from application.chatbot_server.routers import account, chatbot, test
from fastapi.middleware.cors import CORSMiddleware

from template.base.template_context import TemplateContext
from template.base.template_type import TemplateType
from template.account.account_template_impl import AccountTemplateImpl
from template.chatbot.chatbot_template_impl import ChatbotTemplateImpl

import json
import os
from dotenv import load_dotenv
from service.cache.cache_config import CacheConfig
from service.cache.async_session import init_cache
from service.db.database import MySQLPool
from service.http.http_client import HTTPClientPool

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 템플릿 등록
    TemplateContext.add_template(TemplateType.ACCOUNT, AccountTemplateImpl())
    TemplateContext.add_template(TemplateType.CHATBOT, ChatbotTemplateImpl())

    # 캐시(Redis) 초기화
    cache_config = CacheConfig(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        session_expire_time=int(os.getenv("REDIS_SESSION_EXPIRE", 3600))
    )
    init_cache(cache_config)

    # 글로벌 DB 풀 초기화
    app.state.globaldb = MySQLPool()
    await app.state.globaldb.init(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        db=os.getenv("DB_NAME", "medichain_global")
    )
    print(os.getenv("DB_HOST", "localhost"), os.getenv("DB_PORT", 3306), os.getenv("DB_USER", "root"), os.getenv("DB_PASSWORD", ""), os.getenv("DB_NAME", "medichain_global"))

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
    app.state.category_server_url = os.getenv("CATEGORY_SERVER_URL", "http://localhost:8001")
    
    yield
    # (필요시 종료 코드)

app = FastAPI(lifespan=lifespan)

# --- CORS 미들웨어 추가 ---
# 환경변수에서 허용할 도메인 목록을 가져옴
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    # allow_origins=allowed_origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test.router, prefix="/test", tags=["test"])
app.include_router(account.router, prefix="/account", tags=["account"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])

@app.get("/")
def root():
    return {"message": "Chatbot Server is running"} 
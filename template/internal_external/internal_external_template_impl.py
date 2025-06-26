# from template.base.template.internal_external_template import InternalExternalTemplate
from template.internal_external.common.internal_external_serialize import InternalExternalAskRequest, InternalExternalAskResponse

import os
import asyncio
from dotenv import load_dotenv
    
from service.lang_chain.internal_external_lang_chain import (
    load_embedding_model,
    load_faiss_index,
    load_chunks,
    build_rag_chain,
    get_rag_answer_async
)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INDEX_PATH = os.getenv("INTERNAL_EXTERNAL_VECTORDB_INDEX")
CHUNK_PATH = os.getenv("INTERNAL_EXTERNAL_VECTORDB_TXT")
print(f"Using INDEX_PATH: {INDEX_PATH}")
print(f"Using CHUNK_PATH: {CHUNK_PATH}")
# INDEX_PATH = "resources/vectorDB/uiheon/QA_random_pair_part1_index1.index"
# CHUNK_PATH = "resources/vectorDB/uiheon/QA_random_pair_part1_chunks1.txt"

class InternalExternalTemplateImpl:
    def __init__(self):
        self.embed_model = load_embedding_model()
        self.index = load_faiss_index(INDEX_PATH)
        self.chunks = load_chunks(CHUNK_PATH)
        self.rag_chain = build_rag_chain(OPENAI_API_KEY)
    
    def init(self, config=None):
        """초기화 메서드"""
        print("Internal External Template initialized")
        
    def on_load_data(self, config):
        """응급 지원 데이터 로딩"""
        print("Emergency Support data loaded")
        
    def on_client_create(self, db_client, client_session):
        """클라이언트 생성 시 콜백"""
        print("Emergency Support client created")
        
    def on_client_update(self, db_client, client_session):
        """클라이언트 업데이트 시 콜백"""
        print("Emergency Support client updated")
        
    def on_client_delete(self, db_client, user_id):
        """클라이언트 삭제 시 콜백"""
        print("Emergency Support client deleted")

    async def on_internal_external_ask_req(self, client_session, request: InternalExternalAskRequest) -> InternalExternalAskResponse:
        question = request.question
        answer = await get_rag_answer_async(
            question=question,
            index=self.index,
            chunks=self.chunks,
            embed_model=self.embed_model,
            rag_chain=self.rag_chain
        )
        response = InternalExternalAskResponse(answer=answer)
        return response
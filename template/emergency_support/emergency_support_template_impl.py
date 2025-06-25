from template.base.template.emergency_support_template import EmergencySupportTemplate
from template.emergency_support.common.emergency_support_serialize import EmergencySupportAskRequest, EmergencySupportAskResponse
# .\venv\Scripts\Activate.ps1
import os
import asyncio
from dotenv import load_dotenv

# rag_module.py에서 정의한 모든 함수들을 가져옵니다.
# from service.lang_chain.lang_chain import * 선택
from service.lang_chain.lang_chain import (
    load_embedding_model,
    load_faiss_index,
    load_chunks,
    build_rag_chain,
    get_rag_answer_async
)

# 1. 환경 변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 2. 임베딩 파일 및 데이터 경로 정의 (여기서 경로를 지정)
INDEX_PATH = "resources/vectorDB/2wnsqo/QA_random_pair_part2_index1.index"
CHUNK_PATH = "resources/vectorDB/2wnsqo/QA_random_pair_part2_chunks1.txt"

class EmergencySupportTemplateImpl(EmergencySupportTemplate):
    def init(self, config):
        """응급 지원 템플릿 초기화"""
        # print("Emergency Support template initialized")
        # 템플릿이 초기화될 때 RAG 리소스를 로드합니다.
        # 이렇게 하면 모듈을 임포트할 때마다 리소스를 로드하는 것을 방지할 수 있습니다.
        self.embed_model = load_embedding_model()
        self.index = load_faiss_index(INDEX_PATH)
        self.chunks = load_chunks(CHUNK_PATH)
        self.rag_chain = build_rag_chain(OPENAI_API_KEY)
        
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

    async def on_emergency_support_ask_req(self, client_session, request: EmergencySupportAskRequest) -> EmergencySupportAskResponse:
        # 응급 지원 질의 처리
        question = request.question
        answer = await get_rag_answer_async(
            question=question,
            index=self.index,
            chunks=self.chunks,
            embed_model=self.embed_model,
            rag_chain=self.rag_chain
        )
        response = EmergencySupportAskResponse(answer=answer)
        return response 
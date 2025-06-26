from template.base.template.drug_template import DrugTemplate
from template.drug.common.drug_serialize import DrugAskRequest, DrugAskResponse
from service.lang_chain.drug_lang_chain import Vector_store
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

INDEX_PATH = "resources/vectorDB/drug_vectorDB/pilsu_pro_no_prepro_index1.faiss"
CHUNK_PATH = "resources/vectorDB/drug_vectorDB/pilsu_pro_no_prepro_chunks1.txt"

class DrugTemplateImpl(DrugTemplate):
    def init(self, config):
        """약물 템플릿 초기화"""
        print("Drug template initialized")
        
    def on_load_data(self, config):
        """약물 데이터 로딩"""
        print("Drug data loaded")
        
    def on_client_create(self, db_client, client_session):
        """클라이언트 생성 시 콜백"""
        print("Drug client created")
        
    def on_client_update(self, db_client, client_session):
        """클라이언트 업데이트 시 콜백"""
        print("Drug client updated")
        
    def on_client_delete(self, db_client, user_id):
        """클라이언트 삭제 시 콜백"""
        print("Drug client deleted")

    async def on_drug_ask_req(self, client_session, request: DrugAskRequest) -> DrugAskResponse:
        # Vector_store 인스턴스 생성
        vs = Vector_store(
            api_key = OPENAI_API_KEY,
            chunk_path =  CHUNK_PATH,
            index_path = INDEX_PATH,
            )
        # 질문 추출
        question = request.question
        # 답변 생성
        answer = vs.rag_answer(question)
        response = DrugAskResponse(answer=answer)
        return response 
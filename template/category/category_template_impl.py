from template.base.template.category_template import CategoryTemplate
from template.category.common.category_serialize import CategoryAskRequest, CategoryAskResponse
from service.lang_chain.category_classifer import Category_Classifier
from dotenv import load_dotenv
from service.http.http_client import HTTPClientPool
import os
import asyncio
import inspect

load_dotenv()
CATEGORY_URLS = {
    "emergency_support": os.getenv("EMERGENCY_SUPPORT_URL"),
    "internal_external": os.getenv("INTERNAL_EXTERNAL_URL"),
    "drug": os.getenv("DRUG_URL"),
    "clinic": os.getenv("CLINIC_URL"),
}

class CategoryTemplateImpl(CategoryTemplate):
    def __init__(self): # Changed from init to __init__
        """카테고리 템플릿 초기화 및 공유 리소스 로드"""
        super().__init__() # Call parent constructor if CategoryTemplate has one
        self.category_classifier = Category_Classifier() # Category_Classifier 인스턴스를 한 번만 생성
        self.http_client_pool = HTTPClientPool() # HTTPClientPool 인스턴스를 한 번만 생성
        print("Category template initialized")
        
    # If the framework still calls an 'init' method, it can be kept as a no-op or for logging
    def init(self, config):
        print("Category template init hook called (attributes already initialized in __init__)")

    def on_load_data(self, config):
        """카테고리 데이터 로딩"""
        print("Category data loaded")
        
    def on_client_create(self, db_client, client_session):
        """클라이언트 생성 시 콜백"""
        print("Category client created")
        
    def on_client_update(self, db_client, client_session):
        """클라이언트 업데이트 시 콜백"""
        print("Category client updated")
        
    def on_client_delete(self, db_client, user_id):
        """클라이언트 삭제 시 콜백"""
        print("Category client deleted")

    async def on_category_ask_req(self, client_session, request: CategoryAskRequest) -> CategoryAskResponse:
        question = request.question
        category = self.category_classifier.return_category(user_input=question)
        print(f"Classified category: '{category}'")  # 분류된 카테고리 로그
        url = CATEGORY_URLS.get(category)
        print(f"Looked up URL: '{url}' for category '{category}'") # 찾은 URL 로그
        if url:
            # HTTP 요청에 대한 오류 처리 추가
            try:
                category_req = CategoryAskRequest(question=question)
                resp = await self.http_client_pool.post(
                    f"{url}/category/ask",
                    json=category_req.model_dump()
                )
                resp.raise_for_status()
                if inspect.iscoroutinefunction(resp.json):
                    category_resp_json = await resp.json()
                else:
                    category_resp_json = resp.json()
                category_answer = category_resp_json.get("answer", "")
            except Exception as e:
                print(f"Error calling external service {url}: {e}")
                category_answer = f"죄송합니다. 서비스 연결에 문제가 발생했습니다. ({e})"
            response = CategoryAskResponse(answer=category_answer)
        else:
            print(f"No matching URL found for category '{category}'. Returning empty answer.") # URL을 찾지 못했을 때 로그
            response = CategoryAskResponse(answer="")
        return response

        # http://127.0.0.1:8000/internal_external_server/ask
        # http://127.0.0.1:8000/drug_server/ask 
        # http://127.0.0.1:8000/clinic_server/ask
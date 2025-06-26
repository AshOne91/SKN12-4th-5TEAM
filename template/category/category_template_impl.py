from template.base.template.category_template import CategoryTemplate
from template.category.common.category_serialize import CategoryAskRequest, CategoryAskResponse
from service.lang_chain.category_classifer import Category_Classifier
from dotenv import load_dotenv
from service.http.http_client import HTTPClientPool
import os

load_dotenv()
CATEGORY_MAPPING = os.getenv("CATEGORY_MAPPING")

class CategoryTemplateImpl(CategoryTemplate):
    def init(self, config):
        """카테고리 템플릿 초기화"""
        print("Category template initialized")
        
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
        cc = Category_Classifier()
        answer = cc.return_category(user_input=question)
        # if answer != '':
        #     http = HTTPClientPool()
        #     http.post(url=CATEGORY_MAPPING[answer])
        response = CategoryAskResponse(answer=answer)

        return response
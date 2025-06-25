from template.base.template.category_template import CategoryTemplate
from template.category.common.category_serialize import CategoryAskRequest, CategoryAskResponse

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
        # 카테고리 질의 처리
        question = request.question
        # TODO: 실제 카테고리 분류 로직 구현
        answer = f"카테고리 질의: {question}에 대한 응답입니다."
        response = CategoryAskResponse(answer=answer)
        return response 
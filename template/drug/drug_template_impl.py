from template.base.template.drug_template import DrugTemplate
from template.drug.common.drug_serialize import DrugAskRequest, DrugAskResponse

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
        # 약물 질의 처리
        question = request.question
        # TODO: 실제 약물 관련 로직 구현
        answer = f"약물 질의: {question}에 대한 응답입니다."
        response = DrugAskResponse(answer=answer)
        return response 
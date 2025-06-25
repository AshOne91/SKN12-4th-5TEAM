from template.base.template.internal_external_template import InternalExternalTemplate
from template.internal_external.common.internal_external_serialize import InternalExternalAskRequest, InternalExternalAskResponse

class InternalExternalTemplateImpl(InternalExternalTemplate):
    def init(self, config):
        """내과/외과 템플릿 초기화"""
        print("Internal External template initialized")
        
    def on_load_data(self, config):
        """내과/외과 데이터 로딩"""
        print("Internal External data loaded")
        
    def on_client_create(self, db_client, client_session):
        """클라이언트 생성 시 콜백"""
        print("Internal External client created")
        
    def on_client_update(self, db_client, client_session):
        """클라이언트 업데이트 시 콜백"""
        print("Internal External client updated")
        
    def on_client_delete(self, db_client, user_id):
        """클라이언트 삭제 시 콜백"""
        print("Internal External client deleted")

    async def on_internal_external_ask_req(self, client_session, request: InternalExternalAskRequest) -> InternalExternalAskResponse:
        # 내과/외과 질의 처리
        question = request.question
        # TODO: 실제 내과/외과 관련 로직 구현
        answer = f"내과/외과 질의: {question}에 대한 응답입니다."
        response = InternalExternalAskResponse(answer=answer)
        return response 
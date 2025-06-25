from template.base.template.emergency_support_template import EmergencySupportTemplate
from template.emergency_support.common.emergency_support_serialize import EmergencySupportAskRequest, EmergencySupportAskResponse

class EmergencySupportTemplateImpl(EmergencySupportTemplate):
    def init(self, config):
        """응급 지원 템플릿 초기화"""
        print("Emergency Support template initialized")
        
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
        # TODO: 실제 응급 지원 관련 로직 구현
        answer = f"응급 지원 질의: {question}에 대한 응답입니다."
        response = EmergencySupportAskResponse(answer=answer)
        return response 
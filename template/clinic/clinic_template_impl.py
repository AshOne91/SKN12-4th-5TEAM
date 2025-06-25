from template.base.template.clinic_template import ClinicTemplate
from template.clinic.common.clinic_serialize import ClinicAskRequest, ClinicAskResponse

class ClinicTemplateImpl(ClinicTemplate):
    def init(self, config):
        """진료 템플릿 초기화"""
        print("Clinic template initialized")
        
    def on_load_data(self, config):
        """진료 데이터 로딩"""
        print("Clinic data loaded")
        
    def on_client_create(self, db_client, client_session):
        """클라이언트 생성 시 콜백"""
        print("Clinic client created")
        
    def on_client_update(self, db_client, client_session):
        """클라이언트 업데이트 시 콜백"""
        print("Clinic client updated")
        
    def on_client_delete(self, db_client, user_id):
        """클라이언트 삭제 시 콜백"""
        print("Clinic client deleted")

    async def on_clinic_ask_req(self, client_session, request: ClinicAskRequest) -> ClinicAskResponse:
        # 진료 질의 처리
        question = request.question
        # TODO: 실제 진료 관련 로직 구현
        answer = f"진료 질의: {question}에 대한 응답입니다."
        response = ClinicAskResponse(answer=answer)
        return response 
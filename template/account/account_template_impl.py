from template.base.template.account_template import AccountTemplate
from template.account.common.account_serialize import AccountLoginRequest, AccountLoginResponse, AccountLogoutRequest, AccountLogoutResponse, AccountSignupRequest, AccountSignupResponse
from service.cache.async_session import set_session_info, remove_session_info
from template.base.session_info import SessionInfo, ClientSessionState
import uuid
import hashlib, os

class AccountTemplateImpl(AccountTemplate):
    def init(self, config):
        """계정 템플릿 초기화"""
        print("Account template initialized")
        
    def on_load_data(self, config):
        """계정 데이터 로딩"""
        print("Account data loaded")
        
    def on_client_create(self, db_client, client_session):
        """클라이언트 생성 시 콜백"""
        print("Account client created")
        
    def on_client_update(self, db_client, client_session):
        """클라이언트 업데이트 시 콜백"""
        print("Account client updated")
        
    def on_client_delete(self, db_client, user_id):
        """클라이언트 삭제 시 콜백"""
        print("Account client deleted")

    async def on_account_login_req(self, client_session, request: AccountLoginRequest, mysql):
        # DB 프로시저 호출
        result = await mysql.call_procedure("gp_server_platform_auth", (request.id, request.password))
        if not result:
            return AccountLoginResponse(accessToken="", errorCode=401)
        # 로그인 성공 시 토큰 발급 및 세션 저장
        access_token = str(uuid.uuid4())
        session_info = SessionInfo(user_id=request.id, session_state=ClientSessionState.NONE)
        await set_session_info(access_token, session_info)
        return AccountLoginResponse(accessToken=access_token)

    async def on_account_logout_req(self, client_session, request: AccountLogoutRequest):
        access_token = request.accessToken
        await remove_session_info(access_token)
        return AccountLogoutResponse()

    async def on_account_signup_req(self, client_session, request: AccountSignupRequest, mysql):
        # 1. salt 생성 및 비밀번호 해시
        salt = os.urandom(16).hex()
        password_hash = hashlib.sha256((request.password + salt).encode()).hexdigest()
        SHARD_COUNT = 2  # 환경설정에서 관리 가능

        async with mysql.acquire() as conn:
            async with conn.cursor() as cur:
                # 2. 이미 존재하는 아이디 체크
                await cur.execute("CALL GetUserByUsername(%s)", (request.id,))
                if await cur.fetchone():
                    return AccountSignupResponse(errorCode=409, message="이미 사용중인 아이디입니다.")

                # 3. 회원가입(샤드 확정)
                await cur.execute(
                    "CALL RegisterUser(%s, %s, %s, %s, %s, @user_id, @shard_id)",
                    (request.id, request.password, password_hash, salt, SHARD_COUNT)
                )
                await cur.execute("SELECT @user_id, @shard_id")
                row = await cur.fetchone()
                if not row or not row[0]:
                    return AccountSignupResponse(errorCode=500, message="회원가입 실패")
                user_id, shard_id = row

        return AccountSignupResponse(errorCode=0, message="회원가입 성공") 
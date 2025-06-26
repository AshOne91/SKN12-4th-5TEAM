from template.base.template.account_template import AccountTemplate
from template.account.common.account_serialize import AccountLoginRequest, AccountLoginResponse, AccountLogoutRequest, AccountLogoutResponse, AccountSignupRequest, AccountSignupResponse
from service.cache.async_session import set_session_info, remove_session_info
from template.base.session_info import SessionInfo, ClientSessionState
import uuid
import hashlib, os
from service.cache.async_session import set_session_info
from template.base.session_info import SessionInfo, ClientSessionState

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

    async def on_account_login_req(self, client_session, request: AccountLoginRequest, mysql_global, app):
        # 1. username(id)로 유저 조회
        rows = await mysql_global.execute(
            "SELECT user_id, password_hash, salt FROM users WHERE username=%s",
            (request.id,)
        )
        if not rows:
            return AccountLoginResponse(accessToken="", errorCode=404)
        user_id, password_hash, salt = rows[0]["user_id"], rows[0]["password_hash"], rows[0]["salt"]

        # 2. 비밀번호 해시 검증 (SHA256+salt)
        hash_input = (request.password + salt).encode("utf-8")
        hashed = hashlib.sha256(hash_input).hexdigest()
        if hashed != password_hash:
            return AccountLoginResponse(accessToken="", errorCode=401)

        # 3. 샤드 매핑 조회
        rows = await mysql_global.execute(
            "SELECT shard_id FROM user_shard_mapping WHERE user_id=%s",
            (user_id,)
        )
        if not rows:
            return AccountLoginResponse(accessToken="", errorCode=404)
        shard_id = rows[0]["shard_id"]

        # 4. 세션 토큰 생성 및 Redis 저장 (shard_id 포함)
        access_token = str(uuid.uuid4())
        session_info = SessionInfo(user_id=user_id, session_state=ClientSessionState.NONE, shard_id=shard_id)
        await set_session_info(access_token, session_info)

        return AccountLoginResponse(accessToken=access_token, errorCode=0)

    async def on_account_logout_req(self, client_session, request: AccountLogoutRequest):
        access_token = request.accessToken
        await remove_session_info(access_token)
        return AccountLogoutResponse()

    async def on_account_signup_req(self, client_session, request: AccountSignupRequest, mysql_global, app):
        # 1. 중복 아이디 체크
        rows = await mysql_global.execute(
            "SELECT 1 FROM users WHERE username=%s",
            (request.id,)
        )
        if rows:
            return AccountSignupResponse(errorCode=409, message="이미 사용중인 아이디입니다.")

        # 2. salt 생성 및 비밀번호 해시
        salt = os.urandom(16).hex()
        password_hash = hashlib.sha256((request.password + salt).encode()).hexdigest()
        shard_count = len(app.state.userdb_pools)

        # 3. 회원가입(샤드 할당, RegisterUser 프로시저 사용)
        # call_procedure는 DictCursor로 반환하므로 OUT 파라미터는 별도 SELECT 필요
        await mysql_global.execute(
            "CALL RegisterUser(%s, %s, %s, %s, %s, @user_id, @shard_id)",
            (request.id, "", password_hash, salt, shard_count)
        )
        out_rows = await mysql_global.execute("SELECT @user_id as user_id, @shard_id as shard_id")
        if not out_rows or not out_rows[0]["user_id"]:
            return AccountSignupResponse(errorCode=500, message="회원가입 실패")
        user_id, shard_id = out_rows[0]["user_id"], out_rows[0]["shard_id"]

        # 4. 세션 발급(로그인과 동일)
        access_token = str(uuid.uuid4())
        session_info = SessionInfo(user_id=user_id, session_state=ClientSessionState.NONE, shard_id=shard_id)
        await set_session_info(access_token, session_info)

        return AccountSignupResponse(errorCode=0, message=access_token) 
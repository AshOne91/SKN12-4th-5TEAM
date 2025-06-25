from fastapi import APIRouter, Request
from template.base.template_context import TemplateContext
from template.base.template_type import TemplateType
from template.account.common.account_serialize import (
    AccountLoginRequest, AccountLoginResponse,
    AccountLogoutRequest, AccountLogoutResponse,
    AccountSignupRequest, AccountSignupResponse
)

router = APIRouter()

@router.post("/login", response_model=AccountLoginResponse)
async def account_login(request: AccountLoginRequest, req: Request):
    mysql = req.app.state.mysql
    account_template = TemplateContext.get_template(TemplateType.ACCOUNT)
    if account_template is None:
        raise RuntimeError("AccountTemplateImpl is not registered in TemplateContext")
    # DB 인스턴스를 넘겨서 내부에서 await로 DB 호출
    return await account_template.on_account_login_req(None, request, mysql)

@router.post("/logout", response_model=AccountLogoutResponse)
async def account_logout(request: AccountLogoutRequest):
    account_template = TemplateContext.get_template(TemplateType.ACCOUNT)
    if account_template is None:
        raise RuntimeError("AccountTemplateImpl is not registered in TemplateContext")
    return await account_template.on_account_logout_req(None, request)

@router.post("/signup", response_model=AccountSignupResponse)
async def account_signup(request: AccountSignupRequest, req: Request):
    mysql = req.app.state.mysql
    account_template = TemplateContext.get_template(TemplateType.ACCOUNT)
    if account_template is None:
        raise RuntimeError("AccountTemplateImpl is not registered in TemplateContext")
    # DB 인스턴스를 넘겨서 내부에서 await로 DB 호출
    return await account_template.on_account_signup_req(None, request, mysql)
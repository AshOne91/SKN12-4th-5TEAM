from fastapi import APIRouter
from template.base.template_context import TemplateContext
from template.base.template_type import TemplateType
from template.emergency_support.common.emergency_support_serialize import (
    EmergencySupportAskRequest, EmergencySupportAskResponse
)

router = APIRouter()

@router.post("/ask", response_model=EmergencySupportAskResponse)
async def emergency_support_ask(request: EmergencySupportAskRequest):
    emergency_support_template = TemplateContext.get_template(TemplateType.EMERGENCY_SUPPORT)
    if emergency_support_template is None:
        raise RuntimeError("EmergencySupportTemplateImpl is not registered in TemplateContext")
    return emergency_support_template.on_emergency_support_ask_req(None, request) 
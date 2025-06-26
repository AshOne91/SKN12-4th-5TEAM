from fastapi import APIRouter
from template.base.template_context import TemplateContext
from template.base.template_type import TemplateType
from template.internal_external.common.internal_external_serialize import (
    InternalExternalAskRequest, InternalExternalAskResponse
)

router = APIRouter()

@router.post("/ask", response_model=InternalExternalAskResponse)
async def internal_external_ask(request: InternalExternalAskRequest):
    internal_external_template = TemplateContext.get_template(TemplateType.INTERNAL_EXTERNAL)
    if internal_external_template is None:
        raise RuntimeError("InternalExternalTemplateImpl is not registered in TemplateContext")
    return await internal_external_template.on_internal_external_ask_req(None, request) 
from fastapi import APIRouter
from template.base.template_context import TemplateContext
from template.base.template_type import TemplateType
from template.clinic.common.clinic_serialize import (
    ClinicAskRequest, ClinicAskResponse
)

router = APIRouter()

@router.post("/ask", response_model=ClinicAskResponse)
async def clinic_ask(request: ClinicAskRequest):
    clinic_template = TemplateContext.get_template(TemplateType.CLINIC)
    if clinic_template is None:
        raise RuntimeError("ClinicTemplateImpl is not registered in TemplateContext")
    return clinic_template.on_clinic_ask_req(None, request) 
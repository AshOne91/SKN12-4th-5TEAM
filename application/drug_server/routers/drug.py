from fastapi import APIRouter
from template.base.template_context import TemplateContext
from template.base.template_type import TemplateType
from template.drug.common.drug_serialize import (
    DrugAskRequest, DrugAskResponse
)

router = APIRouter()



@router.post("/ask", response_model=DrugAskResponse)
async def drug_ask(request: DrugAskRequest):
    drug_template = TemplateContext.get_template(TemplateType.DRUG)
    if drug_template is None:
        raise RuntimeError("DrugTemplateImpl is not registered in TemplateContext")
    return await drug_template.on_drug_ask_req(None, request) 
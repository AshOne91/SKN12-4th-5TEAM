from fastapi import APIRouter
from template.base.template_context import TemplateContext
from template.base.template_type import TemplateType
from template.category.common.category_serialize import (
    CategoryAskRequest, CategoryAskResponse
)

router = APIRouter()

@router.post("/ask", response_model=CategoryAskResponse)
async def category_ask(request: CategoryAskRequest):
    category_template = TemplateContext.get_template(TemplateType.CATEGORY)
    if category_template is None:
        raise RuntimeError("CategoryTemplateImpl is not registered in TemplateContext")
    return await category_template.on_category_ask_req(None, request)
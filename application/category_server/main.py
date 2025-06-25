from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_base_server.application.category_server.routers import category

from template.base.template_context import TemplateContext
from template.base.template_type import TemplateType
from template.category.category_template_impl import CategoryTemplateImpl

@asynccontextmanager
async def lifespan(app: FastAPI):
    TemplateContext.add_template(TemplateType.CATEGORY, CategoryTemplateImpl())
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(category.router, prefix="/category", tags=["category"])

@app.get("/")
def root():
    return {"message": "Category Server is running"} 
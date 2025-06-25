from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_base_server.application.internal_external_server.routers import internal_external

from template.base.template_context import TemplateContext
from template.base.template_type import TemplateType
from template.internal_external.internal_external_template_impl import InternalExternalTemplateImpl

@asynccontextmanager
async def lifespan(app: FastAPI):
    TemplateContext.add_template(TemplateType.INTERNAL_EXTERNAL, InternalExternalTemplateImpl())
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(internal_external.router, prefix="/internal-external", tags=["internal-external"])

@app.get("/")
def root():
    return {"message": "Internal & Surgery Server is running"} 